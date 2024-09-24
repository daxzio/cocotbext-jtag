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
from cocotbext.jtag.devices.H3JTAGDevice import H3JTAGDevice
from cocotbext.jtag.clkreset import Reset, Clk
from cocotbext.uart import UartSource, UartSink


class testbench:
    def __init__(self, dut):
        bus = JTAGBus(dut)
        self.jtag = JTAGDriver(bus, period=199)
        self.jtag.add_device(H3JTAGDevice())
#         self.jtag.log.setLevel(logging.DEBUG)
#         self.jtag.random_pause = True
        
#         self.jtag_mon = JTAGMonitor(bus)
#         self.jtag_mon.log.setLevel(logging.DEBUG)
        self.clk = Clk(dut, period=87, clkname="clkin")
        self.reset = Reset(dut, resetname='rst', reset_sense=1, reset_length=400)

        self.uart_source = UartSource(getattr(dut, "uart_rx"), baud=230400, bits=8)
        self.uart_sink   = UartSink(getattr(dut, "uart_tx"), baud=230400, bits=8)

 
@test()
async def test_repeat(dut):
    
    tb = testbench(dut)
    await tb.reset.reset_finished()
#     await tb.jtag.wait_clkn(5)
#     await tb.reset.set_reset()
    await tb.jtag.wait_clkn(5)
    await tb.jtag.read_idcode()
    x = await tb.jtag.read_val(addr='DTMCS')
    print(f"{hex(x)}")
#     await tb.jtag.read_val(0x53817905, 'IDCODE')
#     tb.jtag.explict_ir = True
#     await tb.jtag.read_val(0x53817905, 'IDCODE')
#     await tb.jtag.read_val(0x53817905, 'IDCODE')
# # 
# @test()
# async def test_idcode(dut):
#     tb = testbench(dut)
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(20)
#     await tb.jtag.read_idcode()
#  
# @test()
# async def test_userdata(dut):
#     tb = testbench(dut)
#     tb.jtag.explict_ir = True
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(20)
#     await tb.jtag.read_idcode()
#     await tb.jtag.read_val(0xe6712945, 'USERDATA')
#     val = randint(0, 0xffffffff)
#     await tb.jtag.write_val(val, 'USERDATA')
#     await tb.jtag.read_val(val, 'USERDATA')
#     await tb.jtag.wait_clkn(5)
# 
#     tb.jtag.explict_ir = False
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(10)
#     await tb.jtag.read_idcode()
#     await tb.jtag.read_val(0xe6712945, 'USERDATA')
#     for i in range(64):
#         val = randint(0, 0xffffffff)
#         await tb.jtag.write_val(val, 'USERDATA')
#         await tb.jtag.read_val(val, 'USERDATA')
#         if 0 == randint(0, 4):
#             await tb.jtag.read_idcode()
#     await tb.jtag.wait_clkn(5)
# 
#     tb.jtag.explict_ir = False
#     tb.jtag.random_pause = True
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(10)
#     await tb.jtag.read_idcode()
#     await tb.jtag.read_val(0xe6712945, 'USERDATA')
#     for i in range(64):
#         val = randint(0, 0xffffffff)
#         await tb.jtag.write_val(val, 'USERDATA')
#         await tb.jtag.read_val(val, 'USERDATA')
#         if 0 == randint(0, 4):
#             await tb.jtag.read_idcode()
#     await tb.jtag.wait_clkn(5)
# 
