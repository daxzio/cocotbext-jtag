Quick Start Guide
=================

This guide will help you get started with cocotbext-jtag quickly.

Basic Usage
-----------

1. **Import the required modules:**

.. code-block:: python

   from cocotbext.jtag import JTAGDriver, JTAGBus, JTAGDevice
   from cocotb import test
   from cocotb.triggers import Timer

2. **Create a JTAG device model:**

.. code-block:: python

   class MyJTAGDevice(JTAGDevice):
       def __init__(self):
           super().__init__(name="MyDevice", idcode=0x12345678, ir_len=4)
           self.add_jtag_reg("IDCODE", 32, 0xE)
           self.add_jtag_reg("DATA", 32, 0x1)

3. **Set up the testbench:**

.. code-block:: python

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

Signal Mapping
--------------

The JTAGBus class automatically maps to common JTAG signal names on your DUT:

**Required Signals:**
- ``tck`` - Test Clock
- ``tms`` - Test Mode Select
- ``tdi`` - Test Data Input
- ``tdo`` - Test Data Output

**Optional Signals:**
- ``trst`` - Test Reset (active low)

If your DUT uses different signal names, you can specify a prefix:

.. code-block:: python

   bus = JTAGBus.from_prefix(dut, "jtag_")
   # This will look for jtag_tck, jtag_tms, jtag_tdi, jtag_tdo

Multiple Devices
----------------

To test multiple devices in a JTAG chain:

.. code-block:: python

   class TestBench:
       def __init__(self, dut):
           bus = JTAGBus(dut)
           self.jtag = JTAGDriver(bus)

           # Add multiple devices to chain
           self.jtag.add_device(Device1())
           self.jtag.add_device(Device2())
           self.jtag.add_device(Device3())

           # Operations target device 0 by default
           await self.jtag.read("REGISTER", device=0)
           await self.jtag.write("DATA", 0x1234, device=1)

Custom Timing
-------------

You can customize the JTAG clock timing:

.. code-block:: python

   # Custom clock timing
   jtag = JTAGDriver(bus, period=50, units="ns")

   # Enable explicit IR updates
   jtag.explict_ir = True

   # Add random pauses for stress testing
   jtag.random_pause = True

Next Steps
----------

* See the :doc:`api/index` for detailed API documentation
* Check out the :doc:`examples` for more complex usage patterns
* Look at the test files in the ``tests/`` directory for complete examples
