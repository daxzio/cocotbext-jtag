import logging
from random import randint     
from cocotb import start_soon
from cocotb import test
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.triggers import Timer

from cocotbext.jtag import JTAGDriver
from cocotbext.jtag import JTAGMonitor
from cocotbext.jtag import JTAGDevice
from cocotbext.jtag import JTAGBus
# from cocotbext.jtag.gatedclock import GatedClock

class J1JTAGDevice(JTAGDevice):
    def __init__(self, name='jtaglet1', idcode=0x53817905, ir_len=5):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg('USERDATA', 32, 0x8)
        self.add_jtag_reg('USEROP', 8, 0x9)

class testbench:
    def __init__(self, dut):
        bus = JTAGBus(dut)
        self.jtag = JTAGDriver(bus)
        self.jtag.add_device(J1JTAGDevice())
#         self.jtag.log.setLevel(logging.DEBUG)
        
#         self.jtag_mon = JTAGMonitor(bus)
        
#         self.jtag.devices[0].print_regs()

#         self.clk = self.jtag.bus.tck
        
#         self.rst = dut.rst
#         self.gck = dut.gck
#         self.gc = GatedClock(self.gck, 100, units='ns', gated=False)
#         start_soon(self.gc.start())
        
# @test()
# async def test_fsm_reset(dut):
#     tb = testbench(dut)
#     await tb.jtag.set_reset(400)
#     await tb.jtag.wait_clkn(20)
# #     await tb.jtag.reset_fsm()
# #     await tb.jtag.wait_clkn(20)
# #     tb.jtag.random_pause = True
#     await tb.jtag.read_val(0x53817905, 'IDCODE')
#     await tb.jtag.read_val(0x53817905, 'IDCODE')
#     await tb.jtag.wait_clkn(20)
# #     await tb.jtag.read_idcode()
# #     await tb.jtag.wait_clkn(20)
#     
@test()
async def test_repeat(dut):
    
    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read_val(0x53817905, 'IDCODE')
    await tb.jtag.read_val(0x53817905, 'IDCODE')
    tb.jtag.explict_ir = True
    await tb.jtag.read_val(0x53817905, 'IDCODE')
    await tb.jtag.read_val(0x53817905, 'IDCODE')
# 
@test()
async def test_idcode(dut):
    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read_idcode()
 
@test()
async def test_userdata(dut):
    tb = testbench(dut)
    tb.jtag.explict_ir = True
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read_idcode()
    await tb.jtag.read_val(0xe6712945, 'USERDATA')
    val = randint(0, 0xffffffff)
    await tb.jtag.write_val(val, 'USERDATA')
    await tb.jtag.read_val(val, 'USERDATA')
    await tb.jtag.wait_clkn(5)

    tb.jtag.explict_ir = False
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(10)
    await tb.jtag.read_idcode()
    await tb.jtag.read_val(0xe6712945, 'USERDATA')
    for i in range(64):
        val = randint(0, 0xffffffff)
        await tb.jtag.write_val(val, 'USERDATA')
        await tb.jtag.read_val(val, 'USERDATA')
        if 0 == randint(0, 4):
            await tb.jtag.read_idcode()
    await tb.jtag.wait_clkn(5)

