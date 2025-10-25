M3JTAGDevice
============

.. autoclass:: cocotbext.jtag.devices.M3JTAGDevice.M3JTAGDevice
   :members:
   :undoc-members:
   :show-inheritance:

This device model represents an ARM Cortex-M3 processor JTAG interface.

Registers
---------

* **IDCODE** (0xE): 32-bit device identification code
* **EXTEST** (0x0): 1-bit external test register
* **ABORT** (0x8): 35-bit abort register
* **DPACC** (0xA): 35-bit Debug Port Access register
* **APACC** (0xB): 35-bit Access Port Access register
* **BYPASS** (0xF): 1-bit bypass register
