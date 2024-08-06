"""

Copyright (c) 2024 Daxzio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
# from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb import start_soon
# from cocotb.utils import get_sim_time

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .clkreset import Clk, Reset



class JTAGDriver(CocoTBExtLogger):
    def __init__(
        self,
        dut,
        ir_len = 4,
        period=10,
        logging_enabled=True,
    ):
        CocoTBExtLogger.__init__(self, type(self).__name__, logging_enabled)
        self.log.info("JTAG Driver")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info("Copyright (c) 2024 Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")
        
        self.ir_len = ir_len
        self.period = period

        self.tck = dut.tck
        self.tms = dut.tms
        self.tdi = dut.tdi
        self.tdo = dut.tdo
        self.trst = dut.trst

#         self.indexes = [
#             0xE,
#             0xF,
#         ]
        self.chain = {
            0xE: 32, # IDCODE_OP 
            0xF: 1,  # BYPASS_OP 
        }

        self.clk = Clk(dut, period=self.period, clkname='tck')   
        self.reset = Reset(dut, self.clk, reset_sense=0, resetname='trst', reset_length=10)
        self.tms.setimmediatevalue(0)   
        self.tdi.setimmediatevalue(0)
        
#         self._restart()
# 
#     def _restart(self):
#         pass
#         start_soon(self._xxx())
# #         start_soon(self._edge_sync())

    async def send_val(self, val, index=0):

        self.index = index

#         ir_val = self.indexes[self.index]
        ir_val = self.index
        dr_len = self.chain[ir_val]
        dr_val = val
    
        self.tms.value = 0
        self.tdi.value = 0
        await FallingEdge(self.clk.clk)
        self.tms.value = 1
        await FallingEdge(self.clk.clk)
        await FallingEdge(self.clk.clk)
        self.tms.value = 0
        self.tdi.value = 0
        await FallingEdge(self.clk.clk)
        for i in range(self.ir_len):
            await FallingEdge(self.clk.clk)
            self.tdi.value = (ir_val >> i) & 0x1
        self.tms.value = 1
        await FallingEdge(self.clk.clk)
        await FallingEdge(self.clk.clk)
        await FallingEdge(self.clk.clk)
        self.tms.value = 0
        await FallingEdge(self.clk.clk)
        for i in range(dr_len):
            await FallingEdge(self.clk.clk)
            self.tdi.value = (dr_val >> i) & 0x1
        self.tms.value = 1
        await FallingEdge(self.clk.clk)
        await FallingEdge(self.clk.clk)
        self.tms.value = 0

    async def enable_bypass(self):
        await self.send_val(0x1, 0xf)

    async def disable_bypass(self):
        await self.send_val(0x0, 0xf)
