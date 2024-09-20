# JTAG interface modules for Cocotb

[![Build Status](https://github.com/daxzio/cocotbext-jtag/workflows/Regression%20Tests/badge.svg?branch=main)](https://github.com/daxzio/cocotbext-jtag/actions/)
[![codecov](https://codecov.io/gh/daxzio/cocotbext-jtag/branch/main/graph/badge.svg)](https://codecov.io/gh/daxzio/cocotbext-jtag)
[![PyPI version](https://badge.fury.io/py/cocotbext-jtag.svg)](https://pypi.org/project/cocotbext-jtag)
[![Downloads](https://pepy.tech/badge/cocotbext-jtag)](https://pepy.tech/project/cocotbext-jtag)

GitHub repository: https://github.com/daxzio/cocotbext-jtag

## Introduction

JTAG simulation models for [cocotb](https://github.com/cocotb/cocotb).

## Installation

Installation from pip (release version, stable):

    $ pip install cocotbext-jtag

Installation from git (latest development version, potentially unstable):

    $ pip install https://github.com/daxzio/cocotbext-jtag/archive/main.zip

Installation for active development:

    $ git clone https://github.com/daxzio/cocotbext-jtag
    $ pip install -e cocotbext-jtag

## Documentation and usage examples

See the `tests` directory for complete testbenches using these modules.

### JTAG Driver

The `JTAGDriver` classe implement a JTAG driver and is capable of generating read and write operations against JTAG devices, either singularlly or in a chain.  
To use these modules, import the one you need and connect it to the DUT:

    from cocotbext.jtag import JTAGDriver, JTAGBus

    bus = JTAGBus(dut)
    jtag_driver = JTAGDriver(bus)

The first argument to the constructor accepts an `JTAGBus` object.  These objects are containers for the interface signals and include class methods to automate connections.

