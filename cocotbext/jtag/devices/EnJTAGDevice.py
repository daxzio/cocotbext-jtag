from .. import JTAGDevice


class EnJTAGDevice(JTAGDevice):
    def __init__(self, name="EnduraHulk", idcode=0x1ABCD003, ir_len=4, init=False):
        super().__init__(name, idcode, ir_len, init)
        self.add_jtag_reg("IDCODE", 32, 0x2)
        self.add_jtag_reg("BYPASS", 1, 0xF)
