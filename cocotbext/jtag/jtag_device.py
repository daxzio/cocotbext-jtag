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

    def __init__(self, name="default", idcode=0x00000001, ir_len=4, init=True):
        self.id = self.count
        JTAGDevice.count += 1
        self.name = name
        self.idcode = idcode
        self.ir_len = ir_len
        self.names = {}
        self.addresses = {}
        if init:
            self.add_jtag_reg("IDCODE", 32)
            self.add_jtag_reg("BYPASS", 1)
        self._ir_val_prev = None

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
            print(v)

    def __str__(self):
        return f"Device: {self.id} {self.name} idcode 0x{self.idcode:08x}"
