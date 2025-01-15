import logging
import datetime
from collections import deque
from typing import Deque

from cocotb.triggers import RisingEdge, FallingEdge
from cocotb import start_soon

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .jtag_sm import JTAGRxSm
from .jtag_bus import JTAGBus


class JTAGTXn:
    def __init__(
        self,
        ir_val: int = 0x00,
        dr_cnt: int = 0x00,
        tdi: int = 0x00,
        tdo: int = 0x00,
    ):
        self.ir_val = ir_val
        self.dr_cnt = dr_cnt
        self.tdi = tdi
        self.tdo = tdo

    def __str__(self):
        return f"0x{self.ir_val:x} {self.dr_cnt} tdi 0x{self.tdi:x} tdo 0x{self.tdo:x}"


class JTAGMonitor(CocoTBExtLogger):
    def __init__(
        self,
        bus: JTAGBus,
        logging_enabled: bool = True,
    ) -> None:
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )

        self.log.setLevel(logging.INFO)
        self.log.info("JTAG Monitor")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) 2024-{datetime.datetime.now().year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")

        self.bus = bus
        self.ir_val = 0

        self.queue_txn: Deque[JTAGTXn] = deque()

        start_soon(self._jtag_fsm())
        start_soon(self._reset())

    async def _reset(self) -> None:
        if hasattr(self.bus, "trst"):
            while True:
                await FallingEdge(self.bus.trst)
                self.log.info("TRST Reset Detected")
                self.fsm.state = "TEST_LOGIC_RESET"
                await RisingEdge(self.bus.trst)

    async def _detect_reset(self) -> None:
        count = 0
        while True:
            await RisingEdge(self.bus.tck)
            if 1 == self.bus.tms.value:
                count += 1
                if 5 == count:
                    self.log.info("Test logic Reset Detected")
            else:
                count = 0

    async def _jtag_fsm(self) -> None:
        self.fsm = JTAGRxSm(self.bus)
        while True:
            await RisingEdge(self.bus.tck)
            if "SHIFT_IR" == self.fsm.state:
                self.log.debug(f"{self.fsm.state} {self.fsm.ir_cnt}")
            elif "UPDATE_IR" == self.fsm.state:
                self.log.info(f"{self.fsm.state} 0x{self.fsm.ir_val_in:x}")
                self.ir_val = self.fsm.ir_val_in
            elif "SHIFT_DR" == self.fsm.state:
                self.log.debug(f"{self.fsm.state} {self.fsm.dr_cnt}")
            elif "UPDATE_DR" == self.fsm.state:
                self.log.info(
                    f"{self.fsm.state} tdi 0x{self.fsm.dr_val_in:x} tdo 0x{self.fsm.dr_val_out:x}"
                )
                #                 print(f"0x{self.ir_val:x} {self.fsm.dr_cnt} tdi 0x{self.fsm.dr_val_in:x} tdo 0x{self.fsm.dr_val_out:x}")
                txn = JTAGTXn(
                    self.ir_val,
                    self.fsm.dr_cnt,
                    self.fsm.dr_val_in,
                    self.fsm.dr_val_out,
                )
                self.queue_txn.append(txn)
            else:
                self.log.debug(f"{self.fsm.state}")
            self.fsm.update_state()

    @property
    def empty_txn(self) -> bool:
        return not self.queue_txn
