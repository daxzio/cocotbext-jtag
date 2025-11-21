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
from typing import Union, TYPE_CHECKING, cast

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

# Compatibility imports for cocotb 2.0+
try:
    from cocotb._typing import TimeUnit
except ImportError:
    # cocotb 1.9.2 doesn't have TimeUnit
    TimeUnit = str  # type: ignore[misc,assignment]

try:
    from cocotb.task import Task

    _HAS_TASK_TYPE = True
except ImportError:
    _HAS_TASK_TYPE = False
    if TYPE_CHECKING:
        from typing import Any as Task  # type: ignore[misc,assignment]
    else:
        Task = None  # type: ignore[assignment]


# Detect cocotb version (similar to Blender module version checking)
def _parse_version(version_str: str) -> tuple[int, ...]:
    """Parse version string into tuple for comparison."""
    try:
        parts = version_str.split(".")
        return tuple(int(x) for x in parts[:2] if x.isdigit())
    except (ValueError, AttributeError):
        return (0, 0)


COCOTB_VERSION = _parse_version(cocotb.__version__)


class GatedClock(Clock):
    def __init__(
        self,
        signal,
        period: Union[float, Fraction, Decimal],
        unit: Union[TimeUnit, str, None] = None,
        units: Union[str, None] = None,  # For cocotb 1.9.2 compatibility
        gated: bool = True,
    ):
        # Handle both 'unit' (2.0+) and 'units' (1.9.2) parameters
        if units is not None:
            # cocotb 1.9.2 uses 'units'
            if unit is not None:
                raise ValueError("Cannot specify both 'unit' and 'units' parameters")
            time_param = units
        elif unit is not None:
            # cocotb 2.0+ uses 'unit'
            time_param = unit
        else:
            # Default
            time_param = "step"

        # Call parent Clock.__init__ with appropriate parameter
        if COCOTB_VERSION >= (2, 0):
            Clock.__init__(self, signal, period, cast(TimeUnit, time_param))  # type: ignore[arg-type]
        else:
            # cocotb 1.9.2 uses 'units' parameter (str)
            Clock.__init__(self, signal, period, time_param)  # type: ignore[arg-type]
        self.gated = gated

    def start(self, start_high: bool = True):
        """Start the gated clock.

        In cocotb 2.0+, this returns a Task.
        In cocotb 1.9.2, this returns a coroutine that should be passed to cocotb.start().
        """

        async def drive() -> None:
            if COCOTB_VERSION >= (2, 0):
                # cocotb 2.0+: period is the original value, need to calculate
                period = self.period
                time_unit = cast(TimeUnit, getattr(self, "unit", "step"))

                # Ensure t_high is the same type as period to avoid type errors
                t_high: Union[float, Fraction, Decimal]
                if isinstance(period, Decimal):
                    t_high = period / Decimal(2)
                    timer_high = Timer(t_high, unit=time_unit)
                    timer_low = Timer(period - t_high, unit=time_unit)  # type: ignore[operator]
                elif isinstance(period, Fraction):
                    t_high = period / Fraction(2)
                    timer_high = Timer(t_high, unit=time_unit)
                    timer_low = Timer(period - t_high, unit=time_unit)  # type: ignore[operator]
                else:
                    t_high = period / 2.0
                    timer_high = Timer(t_high, unit=time_unit)
                    timer_low = Timer(period - t_high, unit=time_unit)  # type: ignore[operator]
            else:
                # cocotb 1.9.2: period and half_period are already in sim steps
                # Timer accepts sim steps directly with units='step'
                timer_high = Timer(getattr(self, "half_period", 0), units="step")  # type: ignore[attr-defined,arg-type]
                timer_low = Timer(self.period - getattr(self, "half_period", 0), units="step")  # type: ignore[attr-defined,arg-type]

            if start_high:
                self.signal.value = self.gated
                await timer_high
            while True:
                self.signal.value = 0
                await timer_low
                self.signal.value = self.gated
                await timer_high

        if COCOTB_VERSION >= (2, 0):
            # cocotb 2.0+: return Task
            return cocotb.start_soon(drive())
        else:
            # cocotb 1.9.2: return coroutine (caller should use cocotb.start())
            return drive()
