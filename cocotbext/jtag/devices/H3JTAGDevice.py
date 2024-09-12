from .. import JTAGDevice


class H3JTAGDevice(JTAGDevice):
    def __init__(self, name="Hazard5", idcode=0x70982F89, ir_len=5):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0x1)
        self.add_jtag_reg("DTMCS", 32, 0x10)
        self.add_jtag_reg("DMI", 41, 0x11)
