from random import randint     
from cocotb import start_soon
from cocotb import test
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

from cocotbext.jtag import JTAGDriver

class testbench:
    def __init__(self, dut):
        self.jtag = JTAGDriver(dut)
#         self.jtag.indexes = [
#             0x8,
#             0x9,
#             0xE,
#             0xF,
#         ]
        self.jtag.chain = {
            0x8: 32, # USERDATA_OP
            0x9: 8,  # USEROP_OP 
            0xE: 32, # IDCODE_OP 
            0xF: 1,  # BYPASS_OP 
        }
        self.clk = self.jtag.clk
        
 

@test()
async def test_dut_basic(dut):
    
    tb = testbench(dut)
    await tb.clk.wait_clkn(20)
    await tb.jtag.send_val(0xc3, 0x9)
    await tb.jtag.enable_bypass()
    await tb.jtag.disable_bypass()
    
    await tb.clk.wait_clkn(100)
#     await tb.cr.wait_clkn(100)
