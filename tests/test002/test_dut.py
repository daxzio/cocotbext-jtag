import logging
from random import randint     
from cocotb import start_soon
from cocotb import test
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

from cocotbext.jtag import JTAGDriver
from cocotbext.jtag import JTAGMonitor
from cocotbext.jtag import JTAGDevice
from cocotbext.jtag import JTAGBus

class J1JTAGDevice(JTAGDevice):
    def __init__(self, name='jtaglet1', idcode=0x53817905, ir_len=4):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0xe)
        self.add_jtag_reg('USERDATA', 32, 0x8)
        self.add_jtag_reg('USEROP', 8, 0x9)

class J2JTAGDevice(JTAGDevice):
    def __init__(self, name='jtaglet3', idcode=0xc8215c33, ir_len=5):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0x1e)
        self.add_jtag_reg('USERDATA', 32, 0x8)
        self.add_jtag_reg('USEROP', 8, 0x9)

class J3JTAGDevice(JTAGDevice):
    def __init__(self, name='jtaglet3', idcode=0xa92434cf, ir_len=4):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0xe)
        self.add_jtag_reg('USERDATA', 32, 0x8)
        self.add_jtag_reg('USEROP', 8, 0x9)

class testbench:
    def __init__(self, dut):
        bus = JTAGBus(dut)
        self.jtag = JTAGDriver(bus)
        self.jtag.add_device(J1JTAGDevice())
        self.jtag.add_device(J2JTAGDevice())
        self.jtag.add_device(J3JTAGDevice())
        
        self.jtag.devices[0].print_regs()

        self.jtag_mon = JTAGMonitor(bus)
#         self.jtag_mon.log.setLevel(logging.DEBUG)
        self.jtag_mon.log.setLevel(logging.INFO)
        
# @test()
# async def test_fsm_reset(dut):
#     tb = testbench(dut)
#     await tb.jtag.wait_clkn(20)

@test()
async def test_idcodes(dut):
    
    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read_idcode(0)
    await tb.jtag.read_idcode(1)
    await tb.jtag.read_idcode(2)

    tb.jtag.explict_ir = True
    await tb.jtag.read_val('IDCODE', 0xa92434cf, 2)
    await tb.jtag.read_val('IDCODE', 0xc8215c33, 1)
    await tb.jtag.read_val('IDCODE', 0x53817905, 0)
    
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    tb.jtag.explict_ir = False
    await tb.jtag.read_val('IDCODE', 0xa92434cf, 2)
    await tb.jtag.read_val('IDCODE', 0xc8215c33, 1)
    await tb.jtag.read_val('IDCODE', 0x53817905, 0)
    
@test()
async def test_repeat_basic(dut):
    
    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)

    await tb.jtag.read_val('USERDATA', 0x98754ae7, 2)
    await tb.jtag.read_val('USERDATA', 0x46834257, 1)
    await tb.jtag.read_val('USERDATA', 0xe6712945, 0)

    await tb.jtag.write_val('USERDATA', 0xeeeddff5, 2)
    await tb.jtag.write_val('USERDATA', 0x523a5a21, 1)
    await tb.jtag.write_val('USERDATA', 0xadc5a5de, 0)

    await tb.jtag.read_val('USERDATA', 0xeeeddff5, 2)
    await tb.jtag.read_val('USERDATA', 0x523a5a21, 1)
    await tb.jtag.read_val('USERDATA', 0xadc5a5de, 0)

    await tb.jtag.wait_clkn(20)

@test()
async def test_repeat_extensive(dut):
    
    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    
    vals = [
        0xe6712945,
        0x46834257,
        0x98754ae7,
    ]
    
    tb.jtag.random_pause = True
#     tb.jtag_mon.log.setLevel(logging.DEBUG)
    for i in range(64):
        index0 = randint(0, len(tb.jtag.devices)-1)
        index1 = randint(0, len(tb.jtag.devices)-1)
        await tb.jtag.read_val('USERDATA', vals[index0], index0)
        val = randint(0, 0xffffffff)
        await tb.jtag.write_val('USERDATA', val, index1)
        vals[index1] = val

# #     await tb.jtag.read_val(vals[2], 'USERDATA', 2)
# #     await tb.jtag.read_val(vals[1], 'USERDATA', 1)
# #     await tb.jtag.read_val(vals[0], 'USERDATA', 0)
#     
#     val = randint(0, 0xffffffff)
#     
#     await tb.jtag.wait_clkn(20)

#  @test()
# async def test_idcode(dut):
#     tb = testbench(dut)
#     await tb.jtag.set_reset(4)
#     await tb.clk.wait_clkn(20)
#     await tb.jtag.read_idcode()
#  
# @test()
# async def test_bypass(dut):
#     tb = testbench(dut)
#     await tb.jtag.set_reset(4)
#     await tb.clk.wait_clkn(20)
#     await tb.jtag.enable_bypass()
#     await tb.jtag.disable_bypass()
#     tb.jtag.explict_ir = True
#     await tb.jtag.enable_bypass()
#     await tb.jtag.disable_bypass()
