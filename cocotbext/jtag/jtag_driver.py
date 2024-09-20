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

from random import seed
from math import ceil
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb import start_soon
import logging
from cocotb.triggers import Timer

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .clkreset import Reset
from .gatedclock import GatedClock
from .jtag_sm import JTAGTxSm, JTAGRxSm


class JTAGDriver(CocoTBExtLogger):
    def __init__(
        self,
        bus,
        period=100,
        units="ns",
        logging_enabled=True,
    ):
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )
        seed(6)
        self.log.setLevel(logging.INFO)
        self.period = period
        self.units = units
        self.frequency = 1000_000_000 / self.period

        self.log.info("JTAG Driver")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) {self.copyright_year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")
        self.log.info(f"    JTAG CLock Frequency: {self.siunits(self.frequency)}Hz")

        self.bus = bus
        self.tx_fsm = JTAGTxSm(self.bus)
        self.rx_fsm = JTAGRxSm(self.bus)

        # start_soon(Clock(self.bus.tck, self.period, units=units).start())
        self.gc = GatedClock(self.bus.tck, self.period, units=units, gated=False)
        start_soon(self.gc.start(start_high=False))

        if hasattr(self.bus, "trst"):
            self.reset = Reset(
                self.bus.trst,
                #                 self.bus.tck,
                reset_sense=0,
                reset_length=10 * self.period,
                units=self.units,
            )
            self.log.info("    JTAG Reset is present")
        else:
            self.log.info("    JTAG Reset is not present")
        self.bus.tms.setimmediatevalue(0)
        self.bus.tdi.setimmediatevalue(0)

        self.explict_ir = False
        self.suppress_log = False
        self.random_pause = False

        self.devices = []
        self.device = 0

        start_soon(self._jtag_fsm())
        start_soon(self._parse_tdo())

    async def wait_clkn(self, length=1):
        for i in range(int(length)):
            if self.gc.gated:
                await RisingEdge(self.bus.tck)
            else:
                await Timer(self.period, units=self.units)

    @property
    def clock_gated(self):
        return self.gc.gated

    @clock_gated.setter
    def clock_gated(self, value):
        self.gc.gated = value

    @property
    def active_device(self):
        return self.devices[self.device]

    @property
    def total_ir_len(self):
        total = 0
        for d in self.devices:
            total += d.ir_len
        return total

    def add_device(self, device):
        self.devices.append(device)

    async def set_reset(self, num=10):
        if hasattr(self, "reset"):
            self.log.debug("JTAG Resetting")
            self.tx_fsm.reset_state()
            self.rx_fsm.reset_state()
            await self.reset.set_reset(num)
        else:
            self.log.warning("JTAG has no reset, doing nothing!")

    async def _jtag_fsm(self):
        while True:
            await RisingEdge(self.bus.tck)
            self.log.debug(self.rx_fsm.state)
            self.rx_fsm.update_state()

    async def _parse_tdo(self):
        while True:
            await RisingEdge(self.bus.tck)
            if "UPDATE_DR" == self.rx_fsm.state:
                mask = (2**self.dr_len) - 1
                self.ret_val = (
                    self.rx_fsm.dr_val_out >> (len(self.devices) - 1 - self.device)
                ) & mask
                if not self.dr_val is None:
                    if not self.ret_val == self.dr_val and not self.write:
                        raise Exception(
                            f"Expected: 0x{self.dr_val:08x} Returned: 0x{self.ret_val:08x}"
                        )

    #                     else:
    #                         self.log.info(f"Test")
    #                 self.log.info('Finish DR')

    async def reset_fsm(self):
        self.clock_gated = True
        self.bus.tms.value = 1
        for i in range(5):
            await FallingEdge(self.bus.tck)
        # self.bus.tms.value = 0
        self.clock_gated = False

    #         self.total_ir_val_prev = None

    async def send_val(self, val=None, addr=0, device=0, write=True):
        self.device = device
        self.write = write
        if isinstance(addr, str):
            addr = self.active_device.names[addr].address
        elif isinstance(addr, int):
            addr = addr
        else:
            raise Exception(f"Unknown format for addr: {addr}")

        self.ir_val = addr
        self.dr_len = self.active_device.addresses[addr].width
        self.dr_val = val
        self.total_dr_val = val << (len(self.devices) - 1 - self.device)
        self.total_dr_len = self.dr_len + len(self.devices) - 1

        if not self.suppress_log:
            irpad = ceil(self.active_device.ir_len / 4)
            drpad = ceil(self.dr_len / 4)
            if self.write:
                self.log.info(
                    f"Device: {self.device} - Addr: 0x{self.ir_val:0{irpad}x}    Write: 0x{self.dr_val:{drpad}x}"
                )
            else:
                self.log.info(
                    f"Device: {self.device} - Addr: 0x{self.ir_val:0{irpad}x} Expected: 0x{self.dr_val:0{drpad}x}"
                )

        self.total_ir_len2 = 0
        self.total_ir_val = 0
        for i, d in reversed(list(enumerate(self.devices))):
            if i == device:
                v = self.ir_val
            else:
                v = self.devices[i].names["BYPASS"].address
            self.total_ir_val += v << self.total_ir_len2
            self.total_ir_len2 += d.ir_len

        #         self.log.info(f"ir_val 0x{self.total_ir_val:x} ir_len {self.total_ir_len} dr_val 0x{self.total_dr_val:x} ir_len {self.total_dr_len}")

        self.tx_fsm.ir_val = self.total_ir_val
        self.tx_fsm.ir_len = self.total_ir_len
        self.tx_fsm.dr_val = self.total_dr_val
        self.tx_fsm.dr_len = self.total_dr_len
        self.tx_fsm.write = self.write
        self.tx_fsm.explict_ir = self.explict_ir
        self.tx_fsm.start = True
        self.clock_gated = True

        if "TEST_LOGIC_RESET" == self.tx_fsm.state and not self.bus.tms.value:
            self.bus.tms.value = True
            await FallingEdge(self.bus.tck)

        self.dr_val_out = 0
        #         index = 0
        while not self.tx_fsm.finished:
            self.log.debug(f"{self.tx_fsm.state}")
            self.tx_fsm.update_state()
            #             await RisingEdge(self.bus.tck)
            await FallingEdge(self.bus.tck)
        #             if 'SHIFT_DR' == self.tx_fsm.state:
        #                 self.dr_val_out = self.dr_val_out + (int(self.bus.tdo) << index)
        # #                 print(index)
        #                 print(f"{index} 0x{self.dr_val_out:08x}")
        #                 index += 1
        #             if 'UPDATE_DR' == self.tx_fsm.state:
        #                 print(f"0x{self.dr_val_out:08x}")
        self.log.debug(f"{self.tx_fsm.state}")
        self.tx_fsm.update_state()
        await FallingEdge(self.bus.tck)

        self.clock_gated = False

    async def write_val(self, val, addr=None, device=0):
        await self.send_val(val, addr, device, write=True)
        self.suppress_log = False

    async def read_val(self, val, addr=None, device=0):
        await self.send_val(val, addr, device, write=False)

    #     async def _parse_tdo2(self, device):
    #         self.ret_val = 0
    #         await RisingEdge(self.bus.tck)
    # #         if
    #
    #         for i in range(len(self.devices) - device - 1):
    #             await RisingEdge(self.bus.tck)
    #         for i in range(self.dr_len):
    #             await RisingEdge(self.bus.tck)
    #             # print(f"{i} {self.bus.tdo.value}")
    #             # self.log.info(f"{i} {self.bus.tdo.value}")
    #             self.ret_val += self.bus.tdo.value << i
    #         #         if not self.suppress_log:
    #         #             self.log.info(f"Device: {self.device} - Addr: 0x{self.ir_val:04x}  Returned: 0x{self.ret_val:08x}")
    # #         if not self.dr_val is None:
    # #             if not self.ret_val == self.dr_val:
    # #                 raise Exception(
    # #                     f"Expected: 0x{self.dr_val:08x} Returned: 0x{self.ret_val:08x}"
    # #                 )
    #         #         print(f"0x{self.ret_val:08x}")
    #         self.suppress_log = False

    #     async def enable_bypass(self, device=0):
    #         raise
    #         self.device = device
    #         self.suppress_log = True
    #         await self.write_val(0x1, "BYPASS", self.device)
    #         self.log.info(f"Device: {self.device} - Enable BYPASS")
    #
    #     async def disable_bypass(self, device=0):
    #         raise
    #         self.device = device
    #         self.suppress_log = True
    #         await self.write_val(0x0, "BYPASS", self.device)
    #         self.log.info(f"Device: {self.device} - Disable BYPASS")

    async def reset_finished(self):
        await self.reset.reset_finished()

    async def read_idcode(self, device=0):
        self.device = device
        self.suppress_log = True
        await self.send_val(
            self.active_device.idcode, "IDCODE", self.device, write=False
        )
        self.idcode = self.ret_val
        self.log.info(f"Device: {self.device} - IDCODE: 0x{self.idcode:08x}")
