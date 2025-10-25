Installation
============

Requirements
------------

* Python 3.8 or higher
* `cocotb <https://github.com/cocotb/cocotb>`_ 1.9.2 or higher

Install from PyPI (Recommended)
-------------------------------

.. code-block:: bash

   pip install cocotbext-jtag

Install from Git (Development Version)
--------------------------------------

.. code-block:: bash

   pip install https://github.com/daxzio/cocotbext-jtag/archive/main.zip

Install for Development
-----------------------

.. code-block:: bash

   git clone https://github.com/daxzio/cocotbext-jtag
   cd cocotbext-jtag
   pip install -e .

Troubleshooting
---------------

If you encounter issues with cocotb version compatibility, ensure you have the correct version:

.. code-block:: bash

   # For cocotb 1.9.2
   pip install "cocotb>=1.9.2,<2.0"

   # For cocotb 2.0+
   pip install "cocotb>=2.0"

Verification
------------

To verify the installation, run the test suite:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=cocotbext

   # Run specific test
   pytest tests/test001/
