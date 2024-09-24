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

from random import seed, randint
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
        self.tx_fsm = JTAGTxSm(self.bus, randint(0, 0xFFFF))
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

#     @property
#     def total_ir_len(self):
#         total = 0
#         for d in self.devices:
#             total += d.ir_len
#         return total

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
            #             self.log.debug(f"{self.rx_fsm.state} {self.rx_fsm.dr_pause}")
            self.rx_fsm.update_state()

    async def _parse_tdo(self):
        while True:
            await RisingEdge(self.bus.tck)
            if "UPDATE_DR" == self.rx_fsm.state:
                mask = (2**self.dr_len) - 1
                self.ret_val = (
                    self.rx_fsm.dr_val_out >> (len(self.devices) - 1 - self.device)
                ) & mask
                self.log.info(
                    f"Device: {self.device} -              Received: 0x{self.ret_val:08x}"
                )
                if not self.dr_val is None:
                    if not self.ret_val == self.dr_val and not self.write:
                        raise Exception(
                            f"Expected: 0x{self.dr_val:08x} Returned: 0x{self.ret_val:08x}"
                        )

    async def reset_fsm(self):
        self.clock_gated = True
        self.bus.tms.value = 1
        for i in range(5):
            await FallingEdge(self.bus.tck)
        # self.bus.tms.value = 0
        self.clock_gated = False

    async def send_val(self, addr, val=None, device=0, write=True):
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
        if val is None:
            self.total_dr_val = None
        else:
            self.total_dr_val = val << (len(self.devices) - 1 - self.device)
        self.total_dr_len = self.dr_len + len(self.devices) - 1

        if not self.suppress_log:
            irpad = ceil(self.active_device.ir_len / 4)
            drpad = ceil(self.dr_len / 4)
            if self.write:
                self.log.info(
                    f"Device: {self.device} - Addr: {hex(self.ir_val):>6}    Write: 0x{self.dr_val:0{drpad}x}"
                )
            else:
                self.log.info(
                    f"Device: {self.device} - Addr: {hex(self.ir_val):>6} Expected: 0x{self.dr_val:0{drpad}x}"
                )

        self.total_ir_len = 0
        self.total_ir_val = 0
        for i, d in reversed(list(enumerate(self.devices))):
            if i == device:
                v = self.ir_val
            else:
                v = self.devices[i].names["BYPASS"].address
            self.total_ir_val += v << self.total_ir_len
            self.total_ir_len += d.ir_len

        self.tx_fsm.ir_val = self.total_ir_val
        self.tx_fsm.ir_len = self.total_ir_len
        self.tx_fsm.dr_val = self.total_dr_val
        self.tx_fsm.dr_len = self.total_dr_len
        self.tx_fsm.write = self.write
        self.tx_fsm.explict_ir = self.explict_ir
        self.tx_fsm.start = True
        self.clock_gated = True

        self.tx_fsm.gen_dr_random(self.random_pause)
        self.tx_fsm.gen_ir_random(self.random_pause)
        if not 0 == self.tx_fsm.dr_pause:
            self.log.info(
                f"DR Delay {self.tx_fsm.dr_delay}, DR Pause {self.tx_fsm.dr_pause}"
            )
        if not 0 == self.tx_fsm.ir_pause:
            self.log.info(
                f"IR Delay {self.tx_fsm.ir_delay}, IR Pause {self.tx_fsm.ir_pause}"
            )

        if "TEST_LOGIC_RESET" == self.tx_fsm.state and not self.bus.tms.value:
            self.bus.tms.value = True
            await FallingEdge(self.bus.tck)

        self.dr_val_out = 0
        while not self.tx_fsm.finished:
            #             self.log.debug(f"{self.tx_fsm.state} {self.tx_fsm.dr_pause} {self.tx_fsm.dr_delay}")
            if "SHIFT_IR" == self.tx_fsm.state:
                self.log.debug(
                    f"{self.tx_fsm.state} {self.tx_fsm.ir_len} {self.tx_fsm.ir_pause} {self.tx_fsm.ir_delay}"
                )
            elif "SHIFT_DR" == self.tx_fsm.state:
                self.log.debug(f"{self.tx_fsm.state} {self.tx_fsm.dr_len}")
            else:
                self.log.debug(f"{self.tx_fsm.state}")
            self.tx_fsm.update_state()
            await FallingEdge(self.bus.tck)

        self.log.debug(f"{self.tx_fsm.state}")
        self.tx_fsm.update_state()
        await FallingEdge(self.bus.tck)

        self.clock_gated = False

    async def write_val(self, addr, val=None, device=0):
        await self.send_val(addr, val, device, write=True)
        self.suppress_log = False

    async def read_val(self, addr, val=None, device=0):
        await self.send_val(addr, val, device, write=False)
        return self.ret_val

    async def reset_finished(self):
        await self.reset.reset_finished()

    async def read_idcode(self, device=0):
        self.device = device
        self.suppress_log = True
        await self.send_val(
            "IDCODE", self.active_device.idcode, device=self.device, write=False
        )
        self.idcode = self.ret_val
        self.log.info(f"Device: {self.device} -                IDCODE: 0x{self.idcode:08x}")
