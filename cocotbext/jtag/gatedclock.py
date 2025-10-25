# Copyright (c) 2013 Potential Ventures Ltd
# Copyright (c) 2013 SolarFlare Communications Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Potential Ventures Ltd,
#       SolarFlare Communications Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL POTENTIAL VENTURES LTD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""A gated clock class."""

from decimal import Decimal
from fractions import Fraction
from typing import Any, Coroutine, Literal, Union, TYPE_CHECKING

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

# Version detection (Blender style)
COCOTB_VERSION = tuple(int(x) for x in cocotb.__version__.split(".")[:2])

# TimeUnit type handling
if TYPE_CHECKING:
    # For type checking, use the most specific type
    TimeUnit = Literal["step", "fs", "ps", "ns", "us", "ms", "sec"]
else:
    # Runtime: choose based on cocotb version
    if COCOTB_VERSION >= (2, 1):
        # cocotb 2.1+: Use typing.Literal directly
        TimeUnit = Literal["step", "fs", "ps", "ns", "us", "ms", "sec"]
    elif COCOTB_VERSION >= (2, 0):
        # cocotb 2.0.x: Import from cocotb._typing
        from cocotb._typing import TimeUnit
    else:
        # cocotb 1.9.2: Use str
        TimeUnit = str  # type: ignore

# LogicObject type handling
if COCOTB_VERSION >= (2, 0):
    from cocotb.handle import LogicObject
else:
    from cocotb.handle import ModifiableObject as LogicObject  # type: ignore


class GatedClock(Clock):
    r"""Simple 50:50 duty cycle clock driver.

    Instances of this class should call its :meth:`start` method
    and pass the coroutine object to one of the functions in :ref:`task-management`.

    This will create a clocking task that drives the signal at the
    desired period/frequency.

    Example:

    .. code-block:: python

        c = Clock(dut.clk, 10, "ns")
        await cocotb.start(c.start())

    Args:
        signal: The clock pin/signal to be driven.
        period: The clock period. Must convert to an even number of
            timesteps.
        units: One of
            ``'step'``, ``'fs'``, ``'ps'``, ``'ns'``, ``'us'``, ``'ms'``, ``'sec'``.
            When *units* is ``'step'``,
            the timestep is determined by the simulator (see :make:var:`COCOTB_HDL_TIMEPRECISION`).

    If you need more features like a phase shift and an asymmetric duty cycle,
    it is simple to create your own clock generator (that you then :func:`~cocotb.start`):

    .. code-block:: python

        async def custom_clock():
            # pre-construct triggers for performance
            high_time = Timer(high_delay, unit="ns")
            low_time = Timer(low_delay, unit="ns")
            await Timer(initial_delay, unit="ns")
            while True:
                dut.clk.value = 1
                await high_time
                dut.clk.value = 0
                await low_time

    If you also want to change the timing during simulation,
    use this slightly more inefficient example instead where
    the :class:`Timer`\ s inside the while loop are created with
    current delay values:

    .. code-block:: python

        async def custom_clock():
            while True:
                dut.clk.value = 1
                await Timer(high_delay, unit="ns")
                dut.clk.value = 0
                await Timer(low_delay, unit="ns")


        high_delay = low_delay = 100
        await cocotb.start(custom_clock())
        await Timer(1000, unit="ns")
        high_delay = low_delay = 10  # change the clock speed
        await Timer(1000, unit="ns")

    .. versionchanged:: 1.5
        Support ``'step'`` as the *units* argument to mean "simulator time step".

    .. versionchanged:: 2.0
        Passing ``None`` as the *units* argument was removed, use ``'step'`` instead.
    """

    def __init__(
        self,
        signal: LogicObject,
        period: Union[float, Fraction, Decimal],
        units: TimeUnit = "step",
        impl: Union[str, None] = None,
        gated: bool = True,
    ):
        """Initialize GatedClock, handling both cocotb 1.9.2 and 2.0.0."""
        self._unit = units  # Store units for cocotb 1.9.2 compatibility

        if COCOTB_VERSION >= (2, 0):
            # cocotb 2.0.0+: Clock accepts 'unit' parameter (singular) and 'impl'
            Clock.__init__(
                self,
                signal,
                period,
                unit=units,  # type: ignore
                impl=impl,  # type: ignore
            )
        else:
            # cocotb 1.9.2: Clock accepts 'units' parameter (plural) and no impl
            Clock.__init__(
                self,
                signal,
                period,
                units=units,  # type: ignore
            )
            # Store impl manually for 1.9.2
            if impl is not None:
                object.__setattr__(self, "impl", impl)

        self.gated = gated

    def start(self, start_high: bool = True) -> Coroutine[Any, Any, None]:  # type: ignore
        r"""Clocking coroutine.  Start driving your clock by :func:`cocotb.start`\ ing a
        call to this.

        Args:
            start_high: Whether to start the clock with a ``1``
                for the first half of the period.
                Default is ``True``.

                    .. versionadded:: 1.3

                    .. versionchanged:: 2.0
                        Removed ``cycles`` arguments for toggling for a finite amount of cyles.
                        Use ``kill()`` on the clock task instead, or implement manually.
        """

        async def drive() -> None:
            t_high = self.period // 2
            t_low = float(self.period) - float(t_high)

            # Create Timer objects with appropriate parameter name for the cocotb version
            if COCOTB_VERSION >= (2, 0):
                timer_high = Timer(t_high, unit=self._unit)  # type: ignore
                timer_low = Timer(t_low, unit=self._unit)  # type: ignore
            else:
                timer_high = Timer(t_high, units=self._unit)  # type: ignore
                timer_low = Timer(t_low, units=self._unit)  # type: ignore

            if start_high:
                self.signal.value = self.gated
                await timer_high
            while True:
                self.signal.value = 0
                await timer_low
                self.signal.value = self.gated
                await timer_high

        return drive()
