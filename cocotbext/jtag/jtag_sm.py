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
from .jtag_bus import JTAGBus

# from enum import Enum
# class JTAGState(Enum):
#     TEST_LOGIC_RESET = 0x0
#     RUN_TEST_IDLE = 0x1
#     SELECT_DR = 0x2
#     CAPTURE_DR = 0x3
#     SHIFT_DR = 0x4
#     EXIT1_DR = 0x5
#     PAUSE_DR = 0x6
#     EXIT2_DR = 0x7
#     UPDATE_DR = 0x8
#     SELECT_IR = 0x9
#     CAPTURE_IR = 0xA
#     SHIFT_IR = 0xB
#     EXIT1_IR = 0xC
#     PAUSE_IR = 0xD
#     EXIT2_IR = 0xE
#     UPDATE_IR = 0xF


class JTAGTxSm:
    def __init__(self, bus: JTAGBus, iseed: int = 9) -> None:
        self.reset_state()
        self.bus = bus
        self.seed = iseed
        seed(self.seed)

    def reset_state(self):
        self.state = "TEST_LOGIC_RESET"
        self.idle_delay = 0
        self.idle_cnt = 0
        self.ir_len = 0
        self.ir_val = 0
        self.ir_pause = 0
        self.ir_delay = 0
        self.ir_val_prev = None
        self.dr_len = 0
        self.dr_val = 0
        self.dr_pause = 0
        self.dr_delay = 0
        self.write = False
        self.finished = False
        self.explict_ir = False
        self.start = False

    def gen_ir_random(self, random: bool = False) -> None:
        self.ir_pause = 0
        self.ir_delay = 0
        if random:
            if 0 == randint(0, 4):
                self.ir_pause = randint(0, self.ir_len) + 1
                self.ir_delay = randint(0, 4) + 1

    def gen_dr_random(self, random: bool = False) -> None:
        self.dr_pause = 0
        self.dr_delay = 0
        if random:
            if 0 == randint(0, 4):
                self.dr_pause = randint(0, self.dr_len) + 1
                self.dr_delay = randint(0, 7) + 1

    def update_state(self) -> None:

        if self.state == "TEST_LOGIC_RESET":
            self.finished = False
            self.bus.tms.value = True
            if self.start:
                self.state = "RUN_TEST_IDLE"
                self.bus.tms.value = False
        elif self.state == "RUN_TEST_IDLE":
            self.finished = False
            self.idle_delay = max(self.idle_delay - 1, 0)
            if self.idle_delay <= 0:
                self.state = "SELECT_DR"
                self.bus.tms.value = True
            else:
                self.state = "RUN_TEST_IDLE"
                self.bus.tms.value = False
            self.start = False
            self.bus.tdi.value = False
        elif self.state == "SELECT_DR":
            if self.ir_val is None:
                self.ir_len = 0
            elif not self.explict_ir and (self.ir_val == self.ir_val_prev):
                self.ir_len = 0
            if self.dr_len <= 0 or self.ir_len > 0:
                self.state = "SELECT_IR"
                self.bus.tms.value = True
            else:
                self.state = "CAPTURE_DR"
                self.bus.tms.value = False
        elif self.state == "CAPTURE_DR":
            self.state = "SHIFT_DR"
            self.bus.tms.value = False
        elif self.state == "SHIFT_DR":
            if self.write:
                self.bus.tdi.value = self.dr_val & 0x1
            else:
                self.bus.tdi.value = False
            if self.dr_val is not None:
                self.dr_val = self.dr_val >> 1
            self.dr_len -= 1
            self.dr_pause -= 1
            self.bus.tms.value = False
            if self.dr_pause == 0 and not 0 == self.dr_delay:
                self.state = "EXIT1_DR"
                self.bus.tms.value = True
            elif self.dr_len <= 0:
                self.state = "EXIT1_DR"
                self.bus.tms.value = True
        elif self.state == "EXIT1_DR":
            if self.dr_pause == 0 and not 0 == self.dr_delay:
                self.state = "PAUSE_DR"
                self.bus.tms.value = False
            else:
                self.state = "UPDATE_DR"
                self.bus.tms.value = True
        elif self.state == "PAUSE_DR":
            self.bus.tms.value = False
            self.dr_delay -= 1
            if self.dr_delay <= 0:
                self.state = "EXIT2_DR"
                self.bus.tms.value = True
        elif self.state == "EXIT2_DR":
            if self.dr_len <= 0:
                self.state = "UPDATE_DR"
                self.bus.tms.value = True
            else:
                self.state = "SHIFT_DR"
                self.bus.tms.value = False
        elif self.state == "UPDATE_DR":
            if self.dr_len <= 0 and self.ir_len <= 0:
                self.state = "RUN_TEST_IDLE"
                self.bus.tms.value = False
                self.finished = True
            else:
                self.state = "SELECT_DR"
                self.bus.tms.value = True
        elif self.state == "SELECT_IR":
            if self.dr_len <= 0 and self.ir_len <= 0:
                self.state = "TEST_LOGIC_RESET"
                self.bus.tms.value = True
            else:
                self.state = "CAPTURE_IR"
                self.bus.tms.value = False
        elif self.state == "CAPTURE_IR":
            self.state = "SHIFT_IR"
            self.bus.tms.value = False
            self.ir_val_prev = self.ir_val
        elif self.state == "SHIFT_IR":
            self.bus.tdi.value = self.ir_val & 0x1
            self.ir_val = self.ir_val >> 1
            self.ir_len -= 1
            self.ir_pause -= 1
            if self.ir_pause == 0 and not 0 == self.ir_delay:
                self.bus.tms.value = True
                self.state = "EXIT1_IR"
            elif self.ir_len <= 0:
                self.bus.tms.value = True
                self.state = "EXIT1_IR"
        elif self.state == "EXIT1_IR":
            if self.ir_pause == 0 and not 0 == self.ir_delay:
                self.state = "PAUSE_IR"
                self.bus.tms.value = False
            else:
                self.state = "UPDATE_IR"
                self.bus.tms.value = True
        elif self.state == "PAUSE_IR":
            self.bus.tms.value = False
            self.ir_delay -= 1
            if self.ir_delay <= 0:
                self.state = "EXIT2_IR"
                self.bus.tms.value = True
        elif self.state == "EXIT2_IR":
            if self.ir_len <= 0:
                self.state = "UPDATE_IR"
                self.bus.tms.value = True
            else:
                self.state = "SHIFT_IR"
                self.bus.tms.value = False
        elif self.state == "UPDATE_IR":
            if self.dr_len <= 0 and self.ir_len <= 0:
                self.state = "RUN_TEST_IDLE"
                self.finished = True
                self.bus.tms.value = False
            else:
                self.state = "SELECT_DR"
                self.bus.tms.value = True


class JTAGRxSm:
    def __init__(self, bus: JTAGBus) -> None:
        self.reset_state()
        self.bus = bus

    def reset_state(self) -> None:
        self.state = "TEST_LOGIC_RESET"
        self.dr_cnt = 0
        self.dr_val_in = 0
        self.dr_val_out = 0
        self.ir_cnt = 0
        self.ir_val_in = 0

    def update_state(self) -> None:

        if self.state == "TEST_LOGIC_RESET" or self.state == "RUN_TEST_IDLE":
            self.dr_cnt = 0
            self.dr_val_in = 0
            self.dr_val_out = 0
            self.ir_cnt = 0
            self.ir_val_in = 0
        elif self.state == "CAPTURE_DR":
            self.dr_cnt = 0
            self.dr_val_in = 0
            self.dr_val_out = 0
        elif self.state == "SHIFT_DR":
            self.dr_val_in += int(self.bus.tdi.value) << self.dr_cnt
            if "x" == self.bus.tdo.value:
                tdo = 0
            else:
                tdo = int(self.bus.tdo.value)
            self.dr_val_out += tdo << self.dr_cnt
            self.dr_cnt += 1
        elif self.state == "UPDATE_DR":
            pass
        elif self.state == "CAPTURE_IR":
            self.ir_cnt = 0
            self.ir_val_in = 0
        elif self.state == "SHIFT_IR":
            self.ir_val_in += int(self.bus.tdi.value) << self.ir_cnt
            self.ir_cnt += 1
        elif self.state == "UPDATE_IR":
            pass

        if self.state == "TEST_LOGIC_RESET":
            if "0" == self.bus.tms.value:
                self.state = "RUN_TEST_IDLE"
        elif self.state == "RUN_TEST_IDLE":
            if "1" == self.bus.tms.value:
                self.state = "SELECT_DR"
            else:
                self.state = "RUN_TEST_IDLE"
        elif self.state == "SELECT_DR":
            if "1" == self.bus.tms.value:
                self.state = "SELECT_IR"
            else:
                self.state = "CAPTURE_DR"
        elif self.state == "CAPTURE_DR":
            if "1" == self.bus.tms.value:
                self.state = "EXIT1_DR"
            else:
                self.state = "SHIFT_DR"
        elif self.state == "SHIFT_DR":
            if "1" == self.bus.tms.value:
                self.state = "EXIT1_DR"
            else:
                self.state = "SHIFT_DR"
        elif self.state == "EXIT1_DR":
            if "1" == self.bus.tms.value:
                self.state = "UPDATE_DR"
            else:
                self.state = "PAUSE_DR"
        elif self.state == "PAUSE_DR":
            if "1" == self.bus.tms.value:
                self.state = "EXIT2_DR"
            else:
                self.state = "PAUSE_DR"
        elif self.state == "EXIT2_DR":
            if "1" == self.bus.tms.value:
                self.state = "UPDATE_DR"
            else:
                self.state = "SHIFT_DR"
        elif self.state == "UPDATE_DR":
            if "1" == self.bus.tms.value:
                self.state = "SELECT_DR"
            else:
                self.state = "RUN_TEST_IDLE"
        elif self.state == "SELECT_IR":
            if "1" == self.bus.tms.value:
                self.state = "TEST_LOGIC_RESET"
            else:
                self.state = "CAPTURE_IR"
        elif self.state == "CAPTURE_IR":
            if "1" == self.bus.tms.value:
                self.state = "EXIT1_IR"
            else:
                self.state = "SHIFT_IR"
        elif self.state == "SHIFT_IR":
            if "1" == self.bus.tms.value:
                self.state = "EXIT1_IR"
            else:
                self.state = "SHIFT_IR"
        elif self.state == "EXIT1_IR":
            if "1" == self.bus.tms.value:
                self.state = "UPDATE_IR"
            else:
                self.state = "PAUSE_IR"
        elif self.state == "PAUSE_IR":
            if "1" == self.bus.tms.value:
                self.state = "EXIT2_IR"
            else:
                self.state = "PAUSE_IR"
        elif self.state == "EXIT2_IR":
            if "1" == self.bus.tms.value:
                self.state = "UPDATE_IR"
            else:
                self.state = "SHIFT_IR"
        elif self.state == "UPDATE_IR":
            if "1" == self.bus.tms.value:
                self.state = "SELECT_DR"
            else:
                self.state = "RUN_TEST_IDLE"
        else:
            raise Exception(f"Unknown state {self.state}")
