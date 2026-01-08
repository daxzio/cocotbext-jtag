Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

Added
~~~~~

* Comprehensive documentation with ReadTheDocs support
* Enhanced docstrings for all public APIs
* Improved README with better examples and installation instructions
* Added ``capture_ir()`` and ``capture_dr()`` methods to ``JTAGDriver`` for accessing captured IR and DR register values

Changed
~~~~~~~

* Updated documentation structure and formatting
* Enhanced error messages and warnings

Fixed
~~~~~

* Various documentation typos and formatting issues

[0.1.1] - 2024-12-19
--------------------

Added
~~~~~

* Initial release
* Basic JTAG driver and monitor functionality
* Support for multiple device chains
* OpenOCD integration
* Pre-built device models for common processors (Cortex-M3, Hazard3)
* Comprehensive test suite
* Support for both cocotb 1.9.2 and 2.0+

Features
~~~~~~~~

* JTAGDriver class with complete TAP controller implementation
* JTAGBus class for easy DUT signal mapping
* JTAGDevice base class for custom device models
* JTAGMonitor for transaction monitoring and debugging
* OCDDriver for OpenOCD server integration
* Clock and reset utilities with version compatibility
* GatedClock implementation for both cocotb versions
