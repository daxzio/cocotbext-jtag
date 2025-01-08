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

from math import ceil


class JTAGReg:
    def __init__(
        self,
        name: str,
        width: int,
        address: int = -1,
        ir_len: int = 4,
        write: bool = False,
    ) -> None:
        self.name = name
        self.width = width
        self.address = address
        self.ir_len = ir_len
        self.write = write
        if -1 == address:
            if "BYPASS" == name:
                self.address = (2**self.ir_len) - 1

    def __str__(self) -> str:
        addrpad = ceil(self.ir_len / 4)
        return f"0x{self.address:0{addrpad}x} {self.name} {self.width} {self.ir_len}"


class JTAGDevice:

    count: int = 0

    def __init__(
        self,
        name: str = "default",
        idcode: int = 0x00000001,
        ir_len: int = 4,
        init: bool = True,
    ) -> None:
        self.id = self.count
        JTAGDevice.count += 1
        self.name: str = name
        self.idcode: int = idcode
        self.ir_len: int = ir_len
        self.names: dict = {}
        self.addresses: dict = {}
        if init:
            self.add_jtag_reg("BYPASS", 1)
        self._ir_val_prev = None
        self.idle_delay = 0

    def add_jtag_reg(
        self,
        name: str,
        width: int,
        address: int = -1,
        write: bool = False,
    ) -> None:
        if not -1 == address:
            if address >= 2**self.ir_len:
                raise Exception(
                    f"Address supplied for {name}, {hex(address)}, is out of range possible for ir_len {self.ir_len}"
                )
        jr = JTAGReg(name, width, address, self.ir_len, write)
        self.names[jr.name] = jr
        self.addresses[jr.address] = jr

    def print_regs(self) -> None:
        print(self)
        for k, v in sorted(self.addresses.items()):
            print(v)

    def __str__(self) -> str:
        return f"Device: {self.id} {self.name} idcode 0x{self.idcode:08x}"
