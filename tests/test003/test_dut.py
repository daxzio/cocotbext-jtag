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


class J1JTAGDevice(JTAGDevice):
    def __init__(self, name="jtaglet1", idcode=0x53817905, ir_len=5):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0x1E)
        self.add_jtag_reg("USERDATA", 32, 0x8)
        self.add_jtag_reg("USEROP", 8, 0x9)


class testbench:
    def __init__(self, dut):
        signals = {
            "tck": "a",
            "tms": "b",
            "tdi": "c",
            "tdo": "d",
        }
        bus = JTAGBus(dut, signals=signals)
        self.jtag = JTAGDriver(bus)
        self.jtag.add_device(J1JTAGDevice())


@test()
async def test_fsm_reset(dut):
    tb = testbench(dut)
    await tb.jtag.set_reset()
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read("USERDATA")
    await tb.jtag.wait_clkn(20)
    await tb.jtag.reset_fsm(7)
    await tb.jtag.wait_clkn(20)

    await tb.jtag.shift_dr(val=0x53817905)

    await tb.jtag.wait_clkn(20)


@test()
async def test_repeat(dut):

    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read("IDCODE", 0x53817905)
    assert tb.jtag.capture_ir() == 1
    await tb.jtag.read("IDCODE", 0x53817905)
    tb.jtag.explict_ir = True
    await tb.jtag.read("IDCODE", 0x53817905)
    await tb.jtag.read("IDCODE", 0x53817905)


@test()
async def test_idcode(dut):
    tb = testbench(dut)
    await tb.jtag.set_reset(4)
    await tb.jtag.wait_clkn(20)
    await tb.jtag.read_idcode()


# @test()
# async def test_userdata(dut):
#     tb = testbench(dut)
#     tb.jtag.explict_ir = True
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(20)
#     await tb.jtag.read_idcode()
#     await tb.jtag.read('USERDATA', 0xe6712945)
#     val = randint(0, 0xffffffff)
#     await tb.jtag.write_val('USERDATA', val)
#     await tb.jtag.read('USERDATA', val)
#     await tb.jtag.wait_clkn(5)
#
#     tb.jtag.explict_ir = False
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(10)
#     await tb.jtag.read_idcode()
#     await tb.jtag.read('USERDATA', 0xe6712945)
#     for i in range(64):
#         val = randint(0, 0xffffffff)
#         await tb.jtag.write_val('USERDATA', val)
#         await tb.jtag.read('USERDATA', val)
#         if 0 == randint(0, 4):
#             await tb.jtag.read_idcode()
#     await tb.jtag.wait_clkn(5)
#
#     tb.jtag.explict_ir = False
#     tb.jtag.random_pause = True
#     await tb.jtag.set_reset(4)
#     await tb.jtag.wait_clkn(10)
#     await tb.jtag.read_idcode()
#     await tb.jtag.read('USERDATA', 0xe6712945)
#     for i in range(64):
#         val = randint(0, 0xffffffff)
#         await tb.jtag.write_val('USERDATA', val)
#         await tb.jtag.read('USERDATA', val)
#         if 0 == randint(0, 4):
#             await tb.jtag.read_idcode()
#     await tb.jtag.wait_clkn(5)
