from .version import __version__
from .cocotbext_logger import CocoTBExtLogger


class JTAGMonitor(CocoTBExtLogger):
    def __init__(
        self,
        bus,
        logging_enabled=True,
    ):
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )

        self.log.info("JTAG Driver")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) {self.copyright_year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")
        #         self.log.info(f"    JTAG CLock Frequency: {self.units(self.frequency)}Hz")

        self.bus = bus
