from .. import JTAGDevice


class M3JTAGDevice(JTAGDevice):
    def __init__(self, name="CortexM3", idcode=0x4BA00477, ir_len=4):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0xE)
        self.add_jtag_reg("EXTEST", 1, 0x0)
        self.add_jtag_reg("ABORT", 35, 0x8)
        self.add_jtag_reg("DPACC", 35, 0xA)
        self.add_jtag_reg("APACC", 35, 0xB)
