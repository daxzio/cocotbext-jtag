from .. import JTAGDevice


class M3JTAGDevice(JTAGDevice):
    """
    Represents a CortexM3 JTAG device.

    Args:
        name (str): The name of the JTAG device. Defaults to "CortexM3".
        idcode (int): The ID code of the JTAG device. Defaults to 0x4BA00477.
        ir_len (int): The length of the instruction register. Defaults to 4.
    """

    def __init__(self, name="CortexM3", idcode=0x4BA00477, ir_len=4):
        """
        Initializes a new instance of the M3JTAGDevice class.
        """
        super().__init__(name, idcode, ir_len)
        self.add_jtag_reg("IDCODE", 32, 0xE)
        self.add_jtag_reg("EXTEST", 1, 0x0)
        self.add_jtag_reg("ABORT", 35, 0x8)
        self.add_jtag_reg("DPACC", 35, 0xA)
        self.add_jtag_reg("APACC", 35, 0xB)
