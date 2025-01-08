from .. import JTAGDevice


class H3JTAGDevice(JTAGDevice):
    def __init__(self, name="Hazard3", idcode=0xDEADBEEF, ir_len=5):
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0x1, False)
        self.add_jtag_reg("DTMCS", 32, 0x10, False)
        #         self.add_jtag_reg("MENTAL", 32, 0x20)
        self.add_jtag_reg("DMI", 41, 0x11, True)
        self.idle_delay = 6
