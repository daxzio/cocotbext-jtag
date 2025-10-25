Contributing
============

We welcome contributions to cocotbext-jtag! This document provides guidelines for contributing to the project.

Getting Started
---------------

1. Fork the repository on GitHub
2. Clone your fork locally:

   .. code-block:: bash

      git clone https://github.com/yourusername/cocotbext-jtag.git
      cd cocotbext-jtag

3. Create a virtual environment:

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4. Install the package in development mode:

   .. code-block:: bash

      pip install -e .

5. Install development dependencies:

   .. code-block:: bash

      pip install pytest pytest-cov flake8

Development Workflow
--------------------

1. Create a feature branch:

   .. code-block:: bash

      git checkout -b feature/amazing-feature

2. Make your changes
3. Add tests for new functionality
4. Run the test suite:

   .. code-block:: bash

      pytest

5. Run linting:

   .. code-block:: bash

      flake8 cocotbext/

6. Commit your changes:

   .. code-block:: bash

      git commit -m "Add amazing feature"

7. Push to your fork:

   .. code-block:: bash

      git push origin feature/amazing-feature

8. Open a Pull Request on GitHub

Coding Standards
----------------

* Follow PEP 8 style guidelines
* Use type hints where appropriate
* Add docstrings to all public functions and classes
* Write tests for new functionality
* Update documentation as needed

Testing
-------

All new code must include tests. The test suite uses pytest and should be run before submitting a PR:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=cocotb

   # Run specific test file
   pytest tests/test001/test_dut.py

Documentation
-------------

* Update docstrings for any new public APIs
* Add examples to the documentation
* Update the README if needed
* Follow the existing documentation style

Pull Request Process
--------------------

1. Ensure all tests pass
2. Update documentation as needed
3. Add a clear description of your changes
4. Reference any related issues
5. Request review from maintainers

Issue Reporting
---------------

When reporting issues, please include:

* Python version
* cocotb version
* Operating system
* Steps to reproduce
* Expected behavior
* Actual behavior
* Error messages or logs

License
-------

By contributing to cocotbext-jtag, you agree that your contributions will be licensed under the MIT License.
