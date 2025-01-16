import socket
import logging
import datetime
from random import seed, randint

# from cocotb import start_soon
from cocotb.triggers import Timer

from .version import __version__
from logging import Logger
from .cocotbext_logger import CocoTBExtLogger
from .jtag_bus import JTAGBus


class OpenOCDClient:
    TCP_SIZE = 256

    def __init__(
        self,
        bus: JTAGBus,
        log: Logger,
        host: str = "localhost",
        port: int = 9999,
        period: int = 1000,
        units: str = "ns",
    ) -> None:
        self.bus = bus
        self.log = log
        self.host = host
        self.port = port
        self.period = period
        self.units = units
        self.rxbuf = b""
        self.txbuf = b""
        self.finish = False

        self.bus.tdi.value = False
        self.bus.tms.value = False
        self.bus.tck.value = False

    def start_socket(self) -> None:
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)

        self.connection, self.address = self.serversocket.accept()

    def stop_socket(self) -> None:
        #         self.send_tx()
        self.serversocket.shutdown(socket.SHUT_RDWR)
        self.serversocket.close()

    def clear_tx(self) -> None:
        self.txbuf = b""

    def recv_rx(self) -> None:
        if not hasattr(self, "connection"):
            raise Exception()
        self.rxbuf = self.connection.recv(self.TCP_SIZE)
        self.log.debug(f" rxbuf: {self.rxbuf!r}")

    def send_tx(self) -> None:
        if not 0 == len(self.txbuf):
            self.connection.send(self.txbuf)
            self.log.debug(f" txbuf: {self.txbuf!r}")
            self.clear_tx()

    #     async def listen(self):
    #         while True:
    #             self.recv_rx()

    async def parse(self) -> None:
        while True:
            self.recv_rx()
            for x in self.rxbuf:
                c = chr(x)
                step = 0
                if "r" == c or "s" == c:
                    #                     print(f"{c} trst reset true")
                    if hasattr(self.bus, "trst"):
                        self.bus.trst.value = False
                        step = 1
                elif "t" == c or "u" == c:
                    self.log.debug(f"{c} trst reset false")
                    raise
                elif c >= "0" and c <= "7":
                    mask = ord(c) - ord("0")
                    self.bus.tdi.value = (mask >> 0) & 0x1
                    self.bus.tms.value = (mask >> 1) & 0x1
                    self.bus.tck.value = (mask >> 2) & 0x1
                    step = 1
                elif "R" == c:
                    if "x" == self.bus.tdo.value:
                        tdo = b"0"
                    else:
                        tdo = str(int(self.bus.tdo.value)).encode()
                    self.txbuf += tdo
                    if len(self.txbuf) >= self.TCP_SIZE:
                        raise
                        self.send_tx()
                elif "Q" == c:
                    self.log.debug(f"{c} OpenOCD sent quit command")
                    self.stop_socket()
                    self.finish = True
                    return
                elif "B" == c:
                    step = randint(0, 8)
                    step = 2
                elif "b" == c:
                    step = randint(0, 8)
                    step = 2
                else:
                    self.log.warning(f"{c} not implemented")
                    raise

                while not 0 == step:
                    await Timer(self.period / 2, units=self.units)
                    step -= 1

            self.send_tx()


class OCDDriver(CocoTBExtLogger):
    def __init__(
        self,
        bus: JTAGBus,
        host="localhost",
        port=9999,
        period=1000,
        units="ns",
        logging_enabled=True,
    ) -> None:
        CocoTBExtLogger.__init__(
            self, type(self).__name__, logging_enabled, start_year=2024
        )
        seed(5)
        self.log.setLevel(logging.INFO)
        self.host = host
        self.port = port
        self.period = period
        self.units = units
        self.frequency = 1000_000_000 / self.period
        self.bus = bus

        self.log.info("OpenOCD JTAG Driver")
        self.log.info(f"cocotbext-jtag version {__version__}")
        self.log.info(f"Copyright (c) 2024-{datetime.datetime.now().year} Daxzio")
        self.log.info("https://github.com/daxzio/cocotbext-jtag")
        self.log.info(f"    JTAG CLock Frequency: {self.siunits(self.frequency)}Hz")
        if hasattr(self.bus, "trst"):
            self.log.info("    JTAG Reset is present")
        else:
            self.log.info("    JTAG Reset is not present")

        self.ocd = OpenOCDClient(
            self.bus, self.log, self.host, self.port, self.period, self.units
        )
        #         start_soon(self._run())
        #         start_soon(self._start_parse())
        #
        #     async def _run(self):
        self.ocd.start_socket()

    async def _start_parse(self):
        await self.ocd.parse()


#         if not self.ocd.finish:
#             await Timer(50, units="us")
