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
from cocotb_bus.bus import Bus

# from cocotb.utils import get_sim_time

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .clkreset import Clk, Reset


class JTAGBus(Bus):
    _signals = [
        "tck",
        "tms",
        "tdi",
        "tdo",
    ]
    _optional_signals = [
        "trst",
    ]

    def __init__(self, entity=None, prefix=None, **kwargs):
        super().__init__(
            entity,
            prefix,
            self._signals,
            optional_signals=self._optional_signals,
            **kwargs,
        )

    @classmethod
    def from_entity(cls, entity, **kwargs):
        return cls(entity, **kwargs)

    @classmethod
    def from_prefix(cls, entity, prefix, **kwargs):
        return cls(entity, prefix, **kwargs)


class JTAGReg:
    def __init__(self, name, width, address=None, ir_len=4):
        self.name = name
        self.width = width
        self.address = address
        self.ir_len = ir_len
        if address is None:
            if "BYPASS" == name:
                self.address = (2**self.ir_len) - 1
            elif "IDCODE" == name:
                self.address = (2**self.ir_len) - 2

    def __str__(self):
        addrpad = ceil(self.ir_len / 4)
        return f"0x{self.address:0{addrpad}x} {self.name} {self.width} {self.ir_len}"


class JTAGDevice:

    count = 0

    def __init__(self, name="default", idcode=0x00000001, ir_len=4):
        self.id = self.count
        JTAGDevice.count += 1
        self.name = name
        self.idcode = idcode
        self.ir_len = ir_len
        self.names = {}
        self.addresses = {}
        self.add_jtag_reg("IDCODE", 32)
        self.add_jtag_reg("BYPASS", 1)
        self._ir_val_prev = None

    @property
    def ir_val_prev(self):
        if self._ir_val_prev is None:
            self._ir_val_prev = self.names["IDCODE"].address
        return self._ir_val_prev

    @ir_val_prev.setter
    def ir_val_prev(self, value):
        self._ir_val_prev = value

    def add_jtag_reg(
        self,
        name,
        width,
        address=None,
    ):
        jr = JTAGReg(name, width, address, self.ir_len)
        self.names[jr.name] = jr
        self.addresses[jr.address] = jr

    def print_regs(self):
        print(self)
        for k, v in sorted(self.addresses.items()):
            #             print(k, v)
            print(v)

    def __str__(self):
        return f"Device: {self.id} {self.name} idcode 0x{self.idcode:08x}"


class M3JTAGDevice(JTAGDevice):
    def __init__(self, name="CortexM3", idcode=0x4BA00477, ir_len=4):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("EXTEST", 1, 0x0)
        self.add_jtag_reg("ABORT", 35, 0x8)
        self.add_jtag_reg("DPACC", 35, 0xA)
        self.add_jtag_reg("APACC", 35, 0xB)


class H3JTAGDevice(JTAGDevice):
    def __init__(self, name="Hazard5", idcode=0x70982603, ir_len=5):
        super().__init__(name, idcode, ir_len)


class JTAGDriver(CocoTBExtLogger):
    def __init__(
        self,
        dut,
        period=100,
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

        self.bus = JTAGBus(dut)

        self.clk = Clk(dut, period=self.period, clkname="tck")
        if hasattr(self.bus, "trst"):
            self.reset = Reset(
                dut, self.clk, reset_sense=0, resetname="trst", reset_length=10
            )
            self.log.info(f"    JTAG Reset is present")
        else:
            self.log.info(f"    JTAG Reset is not present")
        self.bus.tms.setimmediatevalue(0)
        self.bus.tdi.setimmediatevalue(0)

        self.explict_ir = False
        self.suppress_log = False
        self.random_pause = False
        self.device_prev = None

        self.devices = []
        self.device = 0

    async def wait_clkn(self, length=1):
        await self.clk.wait_clkn(length)

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

        self.bus.tms.value = 0
        #         self.bus.tdi.value = 0
        await FallingEdge(self.bus.tck)
        self.bus.tms.value = 1  # Select DR
        # If the IR is the same as the last time we can move straight to DR
        # except if we want it to be explict everyt time. Implicit is the default
        if (
            not (
                self.ir_val == self.active_device.ir_val_prev
                and self.device == self.device_prev
            )
            or self.explict_ir
        ):
            await FallingEdge(self.bus.tck)
            self.bus.tms.value = 1  # Select IR
            await FallingEdge(self.bus.tck)
            self.bus.tdi.value = 0  # ?
            self.bus.tms.value = 0  # Capture IR
            await FallingEdge(self.bus.tck)
            for i, d in reversed(list(enumerate(self.devices))):
                # print(i, device, d.ir_len, self.ir_val)
                for j in range(d.ir_len):
                    await FallingEdge(self.bus.tck)
                    if i == device:
                        self.bus.tdi.value = (self.ir_val >> j) & 0x1  # Shift IR
                    else:
                        self.bus.tdi.value = 1  # Shift IR
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
        self.active_device.ir_val_prev = self.ir_val

    async def write_val(self, val, addr=None, device=0):
        await self.send_val(val, addr, device, write=True)

    async def read_val(self, val, addr=None, device=0):
        await self.send_val(val, addr, device, write=False)

    async def _parse_tdo(self, device):
        self.ret_val = 0
        await RisingEdge(self.bus.tck)
        for i in range(len(self.devices) - device - 1):
            await RisingEdge(self.bus.tck)
        for i in range(self.dr_len):
            await RisingEdge(self.bus.tck)
            #             print(f"{i} {self.bus.tdo.value}")
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
        self.device = device
        self.suppress_log = True
        await self.write_val(0x1, "BYPASS", device)
        self.log.info(f"Device: {self.device} - Enable BYPASS")

    async def disable_bypass(self, device=0):
        self.device = device
        self.suppress_log = True
        await self.write_val(0x0, "BYPASS", device)
        self.log.info(f"Device: {self.device} - Disable BYPASS")

    async def reset_finished(self):
        await self.reset.reset_finished()

    async def read_idcode(self, device=0):
        self.device = device
        self.suppress_log = True
        await self.send_val(self.active_device.idcode, "IDCODE", device, write=False)
        self.idcode = self.ret_val
        self.log.info(f"Device: {self.device} - IDCODE: 0x{self.idcode:08x}")
