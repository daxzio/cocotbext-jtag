import logging
from cocotb.triggers import RisingEdge
from cocotb import start_soon

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .jtag_sm import JTAGRxSm


class JTAGMonitor(CocoTBExtLogger):
    def __init__(
        self,
        bus,
        logging_enabled=True,
    ):
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )

        self.log.setLevel(logging.INFO)
        self.log.info("JTAG Monitor")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) {self.copyright_year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")

        self.bus = bus

        #         start_soon(self._detect_reset())
        start_soon(self._jtag_fsm())

    async def _detect_reset(self):
        count = 0
        while True:
            await RisingEdge(self.bus.tck)
            if 1 == self.bus.tms.value:
                count += 1
                if 5 == count:
                    self.log.info("Test logic Reset Detected")
            else:
                count = 0

    async def _jtag_fsm(self):
        self.fsm = JTAGRxSm()
        while True:
            await RisingEdge(self.bus.tck)
            if "SHIFT_IR" == self.fsm.state:
                self.log.debug(f"{self.fsm.state} {self.fsm.ir_cnt}")
            elif "SHIFT_DR" == self.fsm.state:
                self.log.debug(f"{self.fsm.state} {self.fsm.dr_cnt}")
            else:
                self.log.debug(f"{self.fsm.state}")
            self.fsm.update_state(self.bus)
