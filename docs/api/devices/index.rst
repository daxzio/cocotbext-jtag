Device Models
=============

This section contains pre-built device models for common JTAG devices.

Available Devices
-----------------

.. toctree::
   :maxdepth: 2

   h3_jtag_device
   m3_jtag_device

Creating Custom Devices
-----------------------

To create a custom device model, inherit from the :class:`JTAGDevice` base class:

.. code-block:: python

   from cocotbext.jtag import JTAGDevice

   class MyCustomDevice(JTAGDevice):
       def __init__(self):
           super().__init__(name="MyDevice", idcode=0x12345678, ir_len=4)
           self.add_jtag_reg("IDCODE", 32, 0xE)
           self.add_jtag_reg("DATA", 32, 0x1)
           self.add_jtag_reg("CONTROL", 8, 0x2)
