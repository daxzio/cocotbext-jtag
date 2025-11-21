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
from typing import Union, cast
from warnings import warn

import cocotb
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

# Compatibility imports for cocotb 2.0+
try:
    from cocotb._typing import TimeUnit
except ImportError:
    # cocotb 1.9.2 doesn't have TimeUnit
    TimeUnit = str  # type: ignore[misc,assignment]


# Detect cocotb version (similar to Blender module version checking)
def _parse_version(version_str: str) -> tuple[int, ...]:
    """Parse version string into tuple for comparison."""
    try:
        parts = version_str.split(".")
        return tuple(int(x) for x in parts[:2] if x.isdigit())
    except (ValueError, AttributeError):
        return (0, 0)


COCOTB_VERSION = _parse_version(cocotb.__version__)


class JTAGDriver(CocoTBExtLogger):
    """JTAG TAP Controller Driver for cocotb.

    This class implements a complete JTAG Test Access Port (TAP) controller
    with state machine support. It can perform read and write operations
    against single or multiple JTAG devices in a chain.

    Args:
        bus: JTAG bus interface object containing TCK, TMS, TDI, TDO signals
        period: Clock period in time units (default: 100)
        unit: Time units - "ns", "us", "ms", etc. (default: "ns")
        logging_enabled: Enable debug logging (default: True)

    Example:
        >>> from cocotbext.jtag import JTAGDriver, JTAGBus, JTAGDevice
        >>>
        >>> bus = JTAGBus(dut)
        >>> jtag = JTAGDriver(bus, period=100, units="ns")
        >>> jtag.add_device(MyJTAGDevice())
        >>> await jtag.read_idcode()
    """

    def __init__(
        self,
        bus: JTAGBus,
        period: int = 100,
        unit: str = "ns",
        logging_enabled: bool = True,
    ) -> None:
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )
        seed(6)
        self.log.setLevel(logging.INFO)
        self.period = period
        self.unit = unit
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

        # GatedClock supports both 'unit' (2.0+) and 'units' (1.9.2) parameters
        if COCOTB_VERSION >= (2, 0):
            self.gc = GatedClock(
                self.bus.tck,
                self.period,
                unit=cast(TimeUnit, unit),
                gated=False,
            )
            start_soon(self.gc.start(start_high=False))
        else:
            # cocotb 1.9.2 uses 'units' parameter
            self.gc = GatedClock(
                self.bus.tck,
                self.period,
                units=unit,
                gated=False,
            )
            start_soon(self.gc.start(start_high=False))

        if hasattr(self.bus, "trst"):
            self.reset = Reset(
                self.bus.trst,
                reset_sense=0,
                reset_length=10 * self.period,
                unit=self.unit,
            )

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
                # Handle Timer parameter name differences between cocotb versions
                # This is legitimate version compatibility - not a bug to hide
                try:
                    # Try cocotb 2.0+ syntax first (unit parameter)
                    await Timer(self.period, unit=self.unit)  # type: ignore[arg-type]
                except TypeError:
                    # Fall back to cocotb 1.9.2 syntax (units parameter)
                    await Timer(self.period, units=self.unit)  # type: ignore[arg-type]

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
        """Add a JTAG device to the chain.

        Args:
            device: JTAGDevice instance to add to the chain

        Example:
            >>> jtag.add_device(MyJTAGDevice())
        """
        self.devices.append(device)

    async def set_reset(self, num: int = 10) -> None:
        """Assert JTAG reset for specified duration.

        Args:
            num: Reset duration in clock periods (default: 10)

        Note:
            Issues a warning if TRST signal is not present in the bus.

        Example:
            >>> await jtag.set_reset(20)  # Reset for 20 clock periods
        """
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
        """Write a value to a JTAG register.

        Args:
            addr: Register name (string) or address (int)
            val: Value to write
            ret_val: Expected return value (for verification)
            device: Device index in chain (default: 0)

        Example:
            >>> await jtag.write("DATA", 0x12345678)
            >>> await jtag.write(0x1, 0xDEADBEEF, device=1)
        """
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
        """Read a value from a JTAG register.

        Args:
            addr: Register name (string) or address (int)
            val: Expected value for verification (optional)
            device: Device index in chain (default: 0)

        Returns:
            The value read from the register

        Example:
            >>> value = await jtag.read("DATA")
            >>> await jtag.read("IDCODE", 0x12345678)  # Verify expected value
        """
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
