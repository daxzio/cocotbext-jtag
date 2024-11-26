import logging
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb import start_soon

from .version import __version__
from .cocotbext_logger import CocoTBExtLogger
from .jtag_sm import JTAGRxSm
from .jtag_bus import JTAGBus


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
        self.log.info(f"Copyright (c) {self.copyright_year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")

        self.bus = bus

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
                self.log.debug(f"{self.fsm.state} 0x{self.fsm.ir_val_in:x}")
            elif "SHIFT_DR" == self.fsm.state:
                self.log.debug(f"{self.fsm.state} {self.fsm.dr_cnt}")
            elif "UPDATE_DR" == self.fsm.state:
                self.log.debug(
                    f"{self.fsm.state} tdi 0x{self.fsm.dr_val_in:x} tdo 0x{self.fsm.dr_val_out:x}"
                )
            else:
                self.log.debug(f"{self.fsm.state}")
            self.fsm.update_state()
