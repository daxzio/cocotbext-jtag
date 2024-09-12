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
from cocotb.clock import Clock

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .clkreset import Clk, Reset
from .jtag_bus import JTAGBus


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
        self.period = period
        self.frequency = 1000_000_000 / self.period

        self.log.info("JTAG Driver")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) {self.copyright_year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")
        self.log.info(f"    JTAG CLock Frequency: {self.units(self.frequency)}Hz")

        self.bus = bus

        start_soon(Clock(self.bus.tck, self.period, units=units).start())

        if hasattr(self.bus, "trst"):
            self.reset = Reset(
                self.bus.trst,
                self.bus.tck,
                reset_sense=0,
                reset_length=10,
            )
            self.log.info(f"    JTAG Reset is present")
        else:
            self.log.info(f"    JTAG Reset is not present")
        self.bus.tms.setimmediatevalue(0)
        self.bus.tdi.setimmediatevalue(0)

        self.explict_ir = False
        self.suppress_log = False
        self.random_pause = False
        #         self.device_prev = None
        self.total_ir_val_prev = None

        self.devices = []
        self.device = 0

    #     async def wait_clkn(self, length=1):
    #         await self.clk.wait_clkn(length)

    async def wait_clkn(self, length=1):
        for i in range(int(length)):
            await RisingEdge(self.bus.tck)

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
        await self.reset.set_reset(num)

    async def reset_fsm(self):
        await FallingEdge(self.bus.tck)
        self.bus.tms.value = 1
        for i in range(5):
            await FallingEdge(self.bus.tck)

    async def send_val(self, val=None, addr=0, device=0, write=True):
        self.device = device
        if isinstance(addr, str):
            addr = self.active_device.names[addr].address
        elif isinstance(addr, int):
            addr = addr
        else:
            raise Exception(f"Unknown format for addr: {addr}")

        self.ir_val = addr
        self.dr_len = self.active_device.addresses[addr].width
        self.dr_val = val

        if not self.suppress_log:
            irpad = ceil(self.active_device.ir_len / 4)
            drpad = ceil(self.dr_len / 4)
            self.log.info(
                f"Device: {self.device} - Addr: 0x{self.ir_val:0{irpad}x} Expected: 0x{self.dr_val:0{drpad}x}"
            )

        self.total_ir_len2 = 0
        self.total_ir_val = 0
        for i, d in reversed(list(enumerate(self.devices))):
            if i == device:
                val = self.ir_val
            else:
                val = self.devices[i].names["BYPASS"].address
            self.total_ir_val += val << self.total_ir_len2
            self.total_ir_len2 += d.ir_len

        self.bus.tms.value = 0
        #         self.bus.tdi.value = 0
        await FallingEdge(self.bus.tck)
        self.bus.tms.value = 1  # Select DR
        # If the IR is the same as the last time we can move straight to DR
        # except if we want it to be explict everyt time. Implicit is the default
        if not (self.total_ir_val_prev == self.total_ir_val) or self.explict_ir:
            await FallingEdge(self.bus.tck)
            self.bus.tms.value = 1  # Select IR
            await FallingEdge(self.bus.tck)
            self.bus.tdi.value = 0  # ?
            self.bus.tms.value = 0  # Capture IR
            await FallingEdge(self.bus.tck)

            # print(f"{self.total_ir_len} 0x{self.total_ir_val:04x}")
            for i in range(self.total_ir_len2):
                await FallingEdge(self.bus.tck)

                # self.log.info(f"{i} - {(self.total_ir_val >> i) & 0x1}")
                self.bus.tdi.value = (self.total_ir_val >> i) & 0x1  # Shift IR

            self.bus.tms.value = 1
            await FallingEdge(self.bus.tck)  # Exit1 IR
            await FallingEdge(self.bus.tck)  # Update IR

        await FallingEdge(self.bus.tck)  # Select DR
        self.bus.tms.value = 0
        await FallingEdge(self.bus.tck)  # Capture DR
        if not write:
            start_soon(self._parse_tdo(self.device))
            self.bus.tdi.value = 0
        for i in range(self.dr_len):
            await FallingEdge(self.bus.tck)
            if write:
                self.bus.tdi.value = (self.dr_val >> i) & 0x1  # Shift DR
        for i in range(len(self.devices) - self.device - 1):
            await FallingEdge(self.bus.tck)
        if self.random_pause:
            await FallingEdge(self.bus.tck)

        self.bus.tms.value = 1
        await FallingEdge(self.bus.tck)  # Exit1 DR
        await FallingEdge(self.bus.tck)  # Update DR
        self.bus.tms.value = 0
        await FallingEdge(self.bus.tck)
        await RisingEdge(self.bus.tck)
        #         self.ir_val_prev = self.ir_val
        self.device_prev = self.device
        self.total_ir_val_prev = self.total_ir_val

    async def write_val(self, val, addr=None, device=0):
        await self.send_val(val, addr, device, write=True)
        self.suppress_log = False

    async def read_val(self, val, addr=None, device=0):
        await self.send_val(val, addr, device, write=False)

    async def _parse_tdo(self, device):
        self.ret_val = 0
        await RisingEdge(self.bus.tck)
        for i in range(len(self.devices) - device - 1):
            await RisingEdge(self.bus.tck)
        for i in range(self.dr_len):
            await RisingEdge(self.bus.tck)
            # print(f"{i} {self.bus.tdo.value}")
            # self.log.info(f"{i} {self.bus.tdo.value}")
            self.ret_val += self.bus.tdo.value << i
        #         if not self.suppress_log:
        #             self.log.info(f"Device: {self.device} - Addr: 0x{self.ir_val:04x}  Returned: 0x{self.ret_val:08x}")
        if not self.dr_val is None:
            if not self.ret_val == self.dr_val:
                raise Exception(
                    f"Expected: 0x{self.dr_val:08x} Returned: 0x{self.ret_val:08x}"
                )
        #         print(f"0x{self.ret_val:08x}")
        self.suppress_log = False

    async def enable_bypass(self, device=0):
        raise
        self.device = device
        self.suppress_log = True
        await self.write_val(0x1, "BYPASS", self.device)
        self.log.info(f"Device: {self.device} - Enable BYPASS")

    async def disable_bypass(self, device=0):
        raise
        self.device = device
        self.suppress_log = True
        await self.write_val(0x0, "BYPASS", self.device)
        self.log.info(f"Device: {self.device} - Disable BYPASS")

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
