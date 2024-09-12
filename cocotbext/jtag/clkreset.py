"""

Copyright (c) 2023-2024 Daxzio

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

from cocotb.clock import Clock
from cocotb import start_soon
from cocotb.triggers import RisingEdge, Timer
from cocotb.handle import ModifiableObject


class Clk:
    def __init__(self, dut, period=10, units="ns", clkname="clk"):
#         print(clkname)
#         self.clk = getattr(dut, clkname)
        try:
            self.clk = getattr(dut, clkname)
        except AttributeError:
            self.clk = dut
        self.name = clkname
        self.period = period
        start_soon(Clock(self.clk, self.period, units=units).start())

    async def wait_clkn(self, length=1):
        for i in range(int(length)):
            await RisingEdge(self.clk)


class Reset:
    def __init__(self, dut, clk, reset_length=100, reset_sense=1, resetname="reset"):

        #         if isinstance(dut, ModifiableObject):
        #             self.reset = dut
        #             print(True)
        #         else:
        #             self.reset = getattr(dut, resetname)
        #         self.reset = getattr(dut, resetname)
        try:
            self.reset = getattr(dut, resetname)
        except AttributeError:
            self.reset = dut
#         print(clk)
        self.clk = clk
        self.reset_length = reset_length
        self.reset_sense = reset_sense
        self.finished = False

        self.reset.setimmediatevalue(self.reset_sense)
        start_soon(self.set_reset())

    async def wait_clkn(self, length=1):
        #print(self.clk.name)
        if isinstance(self.clk, Clk):
            await self.clk.wait_clkn(length)
        else:
            for i in range(int(length)):
                await RisingEdge(self.clk)

    async def set_reset(self, reset_length=None):
        if reset_length is None:
            reset_length = self.reset_length
        await self.wait_clkn(reset_length)
        self.reset.value = (self.reset_sense) & 0x1
        self.finished = False
        await self.wait_clkn(reset_length)
        self.reset.value = (~self.reset_sense) & 0x1
        self.finished = True

    async def reset_finished(self):
        while not self.finished:
            await self.clk.wait_clkn()


class ClkReset:
    def __init__(
        self,
        dut,
        period=10,
        clk_freq=None,
        reset_length=100,
        reset_sense=1,
        clkname="clk",
        resetname="reset",
    ):
        self.clk_freq = clk_freq
        if not self.clk_freq is None:
            self.period = 1000 / self.clk_freq
        else:
            self.period = period
        #        #print(f"clock period {self.period} {self.clk_freq}")
        self.clk = Clk(dut, period=self.period, clkname=clkname)
        self.reset = Reset(
            dut,
            self.clk,
            reset_length=reset_length,
            reset_sense=reset_sense,
            resetname=resetname,
        )

    async def wait_clkn(self, length=1):
        await self.clk.wait_clkn(length)

    async def end_test(self, length=10):
        await self.wait_clkn(length)
