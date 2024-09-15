from random import seed, randint     
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
        self.userOp = dut.userOp
        self.userOp_ready = dut.userOp_ready
        self.userData_out = dut.userData_out
        self.userData_in = dut.userData_in
        self.userData_in.setimmediatevalue(0)   
        self.clk = self.jtag.clk
        
 

@test()
async def test_dut_basic(dut):
    seed(7)
    
    tb = testbench(dut)
#     tb.jtag.random_pause = True
    await tb.jtag.reset_finished()
    await tb.clk.wait_clkn(10)
    await tb.jtag.reset_fsm()
    
    await tb.jtag.enable_bypass()
    await tb.jtag.disable_bypass()
    
    assert tb.userOp== 0
    val = randint(0x0, 0xff)
    await tb.jtag.write_val(val, 0x9)
    assert tb.userOp == val

    valx = 0x1beef06b
    await tb.jtag.read_val(valx, 0xe)
    
#     valx = 0x78
#     await tb.jtag.read_val(valx, 0x9)
#     
#     assert tb.userOp == val
# #     assert tb.userData_out == 0
#     val = randint(0x0, 0xffffffff)
#     await tb.jtag.write_val(val, 0x9)
#     assert tb.userOp == val

#     assert tb.userOp == 0
    for i in range(2):
        val = randint(0x0, 0xff)
        await tb.jtag.write_val(val, 0x9)
        assert tb.userOp == val
    
    assert tb.userData_out == 0
    for i in range(2):
        val = randint(0x0, 0xffffffff)
        await tb.jtag.write_val(val, 0x8)
        assert tb.userData_out == val
    
    await tb.clk.wait_clkn(100)
#     await tb.cr.wait_clkn(100)
