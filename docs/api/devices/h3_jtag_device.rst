H3JTAGDevice
============

.. autoclass:: cocotbext.jtag.devices.H3JTAGDevice.H3JTAGDevice
   :members:
   :undoc-members:
   :show-inheritance:

This device model represents a Hazard3 RISC-V processor JTAG interface.

Registers
---------

* **IDCODE** (0x1): 32-bit device identification code
* **DTMCS** (0x10): 32-bit Debug Transport Module Control and Status
* **DMI** (0x11): 41-bit Debug Module Interface (supports write operations)
* **BYPASS** (0x1F): 1-bit bypass register
