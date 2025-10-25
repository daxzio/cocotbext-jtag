Welcome to cocotbext-jtag's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index
   examples
   contributing
   changelog

cocotbext-jtag provides comprehensive JTAG interface support for hardware verification using cocotb. This package includes drivers, monitors, and device models for common JTAG implementations.

Features
--------

* **JTAG Driver**: Complete JTAG TAP controller implementation with state machine
* **JTAG Monitor**: Transaction monitoring and debugging capabilities
* **Device Models**: Pre-built models for common JTAG devices (Cortex-M3, Hazard3, etc.)
* **OpenOCD Integration**: Direct communication with OpenOCD debug servers
* **Flexible Bus Interface**: Easy connection to DUT JTAG interfaces
* **Comprehensive Testing**: Extensive test suite with multiple device examples

Quick Start
-----------

.. code-block:: python

   from cocotbext.jtag import JTAGDriver, JTAGBus, JTAGDevice
   from cocotb import test
   from cocotb.triggers import Timer

   class MyJTAGDevice(JTAGDevice):
       def __init__(self):
           super().__init__(name="MyDevice", idcode=0x12345678, ir_len=4)
           self.add_jtag_reg("IDCODE", 32, 0xE)
           self.add_jtag_reg("DATA", 32, 0x1)

   @test()
   async def test_jtag_basic(dut):
       # Create JTAG bus and driver
       bus = JTAGBus(dut)
       jtag = JTAGDriver(bus)
       jtag.add_device(MyJTAGDevice())

       # Reset and test
       await jtag.set_reset()
       await Timer(100, units='ns')

       # Read IDCODE
       await jtag.read_idcode()

       # Write and read data
       await jtag.write("DATA", 0xDEADBEEF)
       await jtag.read("DATA", 0xDEADBEEF)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
