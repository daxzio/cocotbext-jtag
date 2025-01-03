"""

Copyright (c) 2023-2025 Daxzio

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

from cocotb.clock import Clock
from cocotb import start_soon
from cocotb.triggers import RisingEdge, Timer


class Clk:
    def __init__(
        self, dut, period: int = 10, units: str = "ns", clkname: str = "clk"
    ) -> None:
        try:
            self.clk = getattr(dut, clkname)
        except AttributeError:
            self.clk = dut
        self.name = clkname
        self.period = period
        start_soon(Clock(self.clk, self.period, units=units).start())

    async def wait_clkn(self, length: int = 1) -> None:
        for i in range(int(length)):
            await RisingEdge(self.clk)


class Reset:
    def __init__(
        self,
        dut,
        clk=None,
        reset_length=100,
        reset_sense=1,
        resetname="reset",
        units="ns",
    ):

        try:
            self.reset = getattr(dut, resetname)
        except AttributeError:
            self.reset = dut

        self.clk = clk
        self.reset_length = reset_length
        self.reset_sense = bool(reset_sense)
        self.units = units
        self.finished = False

        self.reset.setimmediatevalue(self.reset_sense)
        start_soon(self.set_reset())

    async def set_reset(self, reset_length=None):
        if reset_length is None:
            reset_length = self.reset_length

        await Timer(reset_length, units=self.units)
        self.reset.value = self.reset_sense
        self.finished = False
        await Timer(reset_length, units=self.units)
        self.reset.value = not (self.reset_sense)
        self.finished = True

    async def reset_finished(self):
        while not self.finished:
            await Timer(10, units=self.units)


class ClkReset:
    def __init__(
        self,
        dut,
        period=10,
        clk_freq=None,
        reset_length=100,
        reset_sense=1,
        clkname="clk",
        resetname="reset",
    ):
        self.clk_freq = clk_freq
        if self.clk_freq is not None:
            self.period = 1000 / self.clk_freq
        else:
            self.period = period
        #        #print(f"clock period {self.period} {self.clk_freq}")
        self.clk = Clk(dut, period=self.period, clkname=clkname)
        self.reset = Reset(
            dut,
            self.clk,
            reset_length=reset_length,
            reset_sense=reset_sense,
            resetname=resetname,
        )

    async def wait_clkn(self, length=1):
        await self.clk.wait_clkn(length)

    async def end_test(self, length=10):
        await self.wait_clkn(length)
