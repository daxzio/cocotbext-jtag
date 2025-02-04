"""

Copyright (c) 2024-2025 Daxzio

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

import logging
import datetime
from random import seed, randint
from math import ceil
from typing import Union
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb import start_soon
from cocotb.triggers import Timer

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .clkreset import Reset
from .gatedclock import GatedClock
from .jtag_sm import JTAGTxSm, JTAGRxSm
from .jtag_bus import JTAGBus
from .jtag_device import JTAGDevice

# from warnings import deprecated
from warnings import warn


class JTAGDriver(CocoTBExtLogger):
    def __init__(
        self,
        bus: JTAGBus,
        period: int = 100,
        units: str = "ns",
        logging_enabled: bool = True,
    ) -> None:
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )
        seed(6)
        self.log.setLevel(logging.INFO)
        self.period = period
        self.units = units
        self.frequency = 1000_000_000 / self.period
        self.bus = bus

        self.log.info("JTAG Driver")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) 2024-{datetime.datetime.now().year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")
        self.log.info(f"    JTAG CLock Frequency: {self.siunits(self.frequency)}Hz")
        if hasattr(self.bus, "trst"):
            self.log.info("    JTAG Reset is present")
        else:
            self.log.info("    JTAG Reset is not present")

        self.tx_fsm = JTAGTxSm(self.bus, randint(0, 0xFFFF))
        self.rx_fsm = JTAGRxSm(self.bus)
        self.ret_val = None

        self.gc = GatedClock(self.bus.tck, self.period, units=units, gated=False, impl='py')
        start_soon(self.gc.start(start_high=False))

        if hasattr(self.bus, "trst"):
            self.reset = Reset(
                self.bus.trst,
                #                 self.bus.tck,
                reset_sense=0,
                reset_length=10 * self.period,
                units=self.units,
            )

        #         self.bus.tms.setimmediatevalue(1)
        #         self.bus.tdi.setimmediatevalue(0)

        self.bus.tms.value = True
        self.bus.tdi.value = False

        self.explict_ir = False
        self.suppress_log = False
        self.random_pause = False

        self.devices: list = []
        self.device = 0
        self.dr_len: int = 0
        self.dr_val: Union[int, None] = 0

        start_soon(self._jtag_fsm())
        start_soon(self._parse_tdo())

    async def wait_clkn(self, length=1) -> None:
        for i in range(int(length)):
            if self.gc.gated:
                await RisingEdge(self.bus.tck)
            else:
                await Timer(self.period, units=self.units)

    @property
    def clock_gated(self) -> bool:
        return self.gc.gated

    @clock_gated.setter
    def clock_gated(self, value: bool) -> None:
        self.gc.gated = value

    @property
    def active_device(self) -> JTAGDevice:
        return self.devices[self.device]

    def add_device(self, device: JTAGDevice) -> None:
        self.devices.append(device)

    async def set_reset(self, num: int = 10) -> None:
        if hasattr(self, "reset"):
            self.log.debug("JTAG Resetting")
            self.tx_fsm.reset_state()
            self.rx_fsm.reset_state()
            await self.reset.set_reset(num)
        else:
            self.log.warning("JTAG has no reset, doing nothing!")

    async def reset_finished(self) -> None:
        await self.reset.reset_finished()

    async def _jtag_fsm(self) -> None:
        while True:
            await RisingEdge(self.bus.tck)
            self.rx_fsm.update_state()

    async def _parse_tdo(self) -> None:
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
                if self.dr_val is not None:
                    if not self.ret_val == self.dr_val and not self.jwrite:
                        raise Exception(
                            f"Expected: 0x{self.dr_val:08x} Returned: 0x{self.ret_val:08x}"
                        )

    async def reset_fsm(self, num: int = 5) -> None:
        self.clock_gated = True
        self.tx_fsm.reset_state()
        self.bus.tms.value = 1
        for i in range(num):
            await FallingEdge(self.bus.tck)
        self.clock_gated = False

    async def send_val(
        self,
        addr: Union[int, str, None],
        val: Union[int, None] = None,
        device: int = 0,
        write: bool = True,
    ) -> None:
        self.device = device
        self.jwrite = write
        if isinstance(addr, str):
            addr = self.active_device.names[addr].address
        elif isinstance(addr, int):
            addr = addr
        elif addr is None:
            addr = addr
        else:
            raise Exception(f"Unknown format for addr: {addr}")

        self.ir_val = addr
        if addr is None:
            self.dr_len = self.shift_dr_num
        else:
            self.dr_len = self.active_device.addresses[addr].width
        self.dr_val = val
        if val is None:
            self.total_dr_val = None
        else:
            self.total_dr_val = val << (len(self.devices) - 1 - self.device)
        self.total_dr_len = self.dr_len + len(self.devices) - 1

        if not self.suppress_log:
            drpad = ceil(self.dr_len / 4)
            exp = ""
            if self.dr_val is not None:
                exp = f" Expected: 0x{self.dr_val:0{drpad}x}"
            if self.ir_val is not None:
                if self.jwrite:
                    self.log.info(
                        f"Device: {self.device} - Addr: {hex(int(self.ir_val)):>6}    Write: 0x{self.dr_val:0{drpad}x}"
                    )
                else:
                    self.log.info(
                        f"Device: {self.device} - Addr: {hex(int(self.ir_val)):>6}{exp}"
                    )

        self.total_ir_len = 0
        self.total_ir_val = 0
        if addr is not None:
            for i, d in reversed(list(enumerate(self.devices))):
                if i == device:
                    if isinstance(self.ir_val, int):
                        v = self.ir_val
                    else:
                        v = 0
                else:
                    v = self.devices[i].names["BYPASS"].address
                self.total_ir_val += v << self.total_ir_len
                self.total_ir_len += d.ir_len

            self.tx_fsm.ir_val = self.total_ir_val
            self.tx_fsm.ir_len = self.total_ir_len
        else:
            self.tx_fsm.ir_val = addr
            self.tx_fsm.ir_len = 0
        self.tx_fsm.dr_val = self.total_dr_val
        self.tx_fsm.dr_len = self.total_dr_len
        self.tx_fsm.idle_delay = self.active_device.idle_delay
        self.tx_fsm.write = self.jwrite
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

        if "TEST_LOGIC_RESET" == self.tx_fsm.state and "0" == self.bus.tms.value:
            self.bus.tms.value = True
            await FallingEdge(self.bus.tck)

        self.dr_val_out = 0
        while not self.tx_fsm.finished:
            if "SHIFT_IR" == self.tx_fsm.state:
                self.log.debug(
                    f"{self.tx_fsm.state} {self.tx_fsm.ir_len} {self.tx_fsm.ir_pause} {self.tx_fsm.ir_delay}"
                )
            elif "SHIFT_DR" == self.tx_fsm.state:
                self.log.debug(f"{self.tx_fsm.state} {self.tx_fsm.dr_len}")
            else:
                self.log.debug(f"{self.tx_fsm.state}")
            await FallingEdge(self.bus.tck)
            self.tx_fsm.update_state()

        self.log.debug(f"{self.tx_fsm.state}")
        await FallingEdge(self.bus.tck)
        self.tx_fsm.update_state()
        self.clock_gated = False
        if self.ret_val is None:
            raise Exception("self.ret_val should not be 'None'")

    async def write(
        self,
        addr: Union[int, str, None],
        val: Union[int, None] = None,
        ret_val: Union[int, None] = None,
        device: int = 0,
    ) -> None:
        await self.send_val(addr, val, device, write=True)
        self.suppress_log = False

    async def write_val(
        self, addr: Union[int, str, None], val: Union[int, None] = None, device: int = 0
    ) -> None:
        warn("This method is deprecated", DeprecationWarning, stacklevel=2)
        await self.write(addr, val, device)

    async def read(
        self, addr: Union[int, str, None], val: Union[int, None] = None, device: int = 0
    ):
        await self.send_val(addr, val, device, write=False)
        return self.ret_val

    async def read_val(
        self, addr: Union[int, str, None], val: Union[int, None] = None, device: int = 0
    ):
        warn("This method is deprecated", DeprecationWarning, stacklevel=2)
        ret_val = await self.read(addr, val, device)
        return ret_val

    async def shift_dr(
        self, num: int = 32, val: Union[int, None] = None, device: int = 0
    ):
        self.shift_dr_num = num
        self.ret_val = None
        await self.send_val(addr=None, val=val, device=device, write=False)
#         if self.ret_val is None:
#             raise
        return self.ret_val

    async def read_idcode(self, device: int = 0) -> None:
        self.device = device
        self.suppress_log = True
        await self.send_val(
            "IDCODE", self.active_device.idcode, device=self.device, write=False
        )
        self.idcode = self.ret_val
        self.log.info(
            f"Device: {self.device} -                IDCODE: 0x{self.idcode:08x}"
        )
