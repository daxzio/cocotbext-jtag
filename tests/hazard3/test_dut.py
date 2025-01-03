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
# from cocotbext.uart import UartSource, UartSink


class testbench:
    def __init__(self, dut):
        bus = JTAGBus(dut)
        self.jtag = JTAGDriver(bus, period=199)
        self.jtag.add_device(H3JTAGDevice())
#         self.jtag.log.setLevel(logging.DEBUG)
#         self.jtag.random_pause = True
        
        self.jtag_mon = JTAGMonitor(bus)
        self.jtag_mon.log.setLevel(logging.DEBUG)
        self.clk = Clk(dut, period=87, clkname="clkin")
        self.reset = Reset(dut, resetname='rst', reset_sense=1, reset_length=400)

#         self.uart_source = UartSource(getattr(dut, "uart_rx"), baud=230400, bits=8)
#         self.uart_sink   = UartSink(getattr(dut, "uart_tx"), baud=230400, bits=8)

    async def read_dtmcs(self):
        x = await self.jtag.read_val('DTMCS')
        y = {
            'version'      : [ 0, 4, 0],
            'abits'        : [ 4, 6, 0],
            'dmistat'      : [10, 2, 0],
            'idle'         : [12, 3, 0],
            'dmireset'     : [16, 1, 1],
            'dmihardreset' : [17, 1, 1],
        }
        version      = (x >>  0) & (2**4)-1
        abits        = (x >>  4) & (2**6)-1
        dmistat      = (x >> 10) & (2**2)-1
        idle         = (x >> 12) & (2**3)-1
        dmireset     = (x >> 16) & (2**1)-1
        dmihardreset = (x >> 17) & (2**1)-1
        print(f"{hex(x)}")
        print(version, abits, dmistat, idle, dmireset, dmihardreset)

    async def read_dmi(self, addr, data=None):
        op = 1
#         val = (addr << 34) + (data << 2) + op
        val = (addr << 34) + (0 << 2) + op
        print(hex(val))
        await self.jtag.send_val('DMI', val)
        x = await self.jtag.read_val('DMI')
        print(hex(x))
 
    async def write_dmi(self, addr, data):
        op = 2
        val = (addr << 34) + (data << 2) + op
        print(hex(val))
        await self.jtag.send_val('DMI', val)
#         x = await self.jtag.read_val('DMI')
#         print(hex(x))
 
@test()
async def test_repeat(dut):
    
    tb = testbench(dut)
    tb.jtag.explict_ir = False
    await tb.reset.reset_finished()
#     await tb.jtag.wait_clkn(5)
#     await tb.reset.set_reset()
    await tb.jtag.wait_clkn(5)
    await tb.jtag.read_idcode()
    await tb.read_dtmcs()

    await tb.write_dmi(0x4, 0x12345)
    await tb.read_dmi(0x4)

#     op = 1
#     addr = 1
#     data = 1
#     val = (addr << 34) + (data << 2) + op
#     print(hex(val))
#     await tb.jtag.send_val('DMI', val)
#     await tb.jtag.send_val('DMI', val)
#     print(hex(tb.jtag.ret_val))
    
#     x = await tb.jtag.send_val('DMI', val)
#     print(hex(tb.jtag.ret_val))
#     x = await tb.jtag.send_val('DMI', 0x0c00000021)
# #     x = await tb.jtag.write_val('DMI', 0x0000000001)
# #     x = await tb.jtag.read_val('DMI')
    await tb.jtag.wait_clkn(5)
    
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
