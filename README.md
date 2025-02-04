# JTAG interface modules for Cocotb

[![Build Status](https://github.com/daxzio/cocotbext-jtag/actions/workflows/test_checkin.yml/badge.svg?branch=main)](https://github.com/daxzio/cocotbext-jtag/actions/)
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

### JTAG Bus

The `JTAGBus` is used to map to a JTAG interface on the `dut`.  These hold instances of bus objects for the individual channels, which are currently extensions of `cocotb_bus.bus.Bus`.  Class methods `from_entity` and `from_prefix` are provided to facilitate signal default name matching. 

#### Required:
* _tck_
* _tms_
* _tdi_
* _tdo_

#### Optional:
* _trst_

### JTAG Driver

The `JTAGDriver` class implement a JTAG driver and is capable of generating read and write operations against JTAG devices, either singularly or in a chain.  

To use these modules, import the one you need and connect it to the DUT:

    from cocotbext.jtag import JTAGDriver, JTAGBus, JTAGDevice

    bus = JTAGBus(dut)
    jtag_driver = JTAGDriver(bus)
    jtag_driver.add_device(JTAGDevice())

The first argument to the constructor accepts an `JTAGBus` object.  These objects are containers for the interface signals and include class methods to automate connections.

Once the module is instantiated, read and write operations can be initiated in a couple of different ways.


#### Additional optional arguments for `JTAGDriver`

* _period_: Clock frequency period of `tck`, default `100`
* _units_: Clock units, default `ns`
* _logging_enabled_: Logging enable, default `True`

#### Methods


* `add_device(device)`: Add device to jtag chain, must be of type `JTAGDevice`
* `set_reset(num)`: Reset for _num_ if _trst_ is present in `JTAGBus`, raise warning if _trst_ is not present
* `reset_finished()`: Asyn wait until reset is finished
* `reset_fsm()`: Send 5 _tck_ pulses while _tms_ is held high in `JTAGBus`, this resets the finite state machine inside a JTAG TAP
* `send_val(addr, val, device, write)`: Send _addr_ to _device_ (default: `0`). The _val_ is used to write if _write_ is True or verify against if _write_ is False
* `write(addr, val, device=0)`: Write _val_ to _addr_ of _device_ (default: `0`). 
* `read(addr, val=None, device=0)`: Read from _addr_ of _device_ (default: `0`). If _val_ present verify against returned value.
* `read_idcode(device)`: Read device number _device_ and confirm it matched the IDCODE set for that device


### JTAG Device

`JTAGDriver` needs to be told what devices are in the JTAG chain it is communicating with inside the `dut`. A `JTAGDevice` needs to be defined for this purpose or a device that inherits from this base class.

A `JTAGDevice` needs a _name_, _idcode_ and _ir_len_.  It also seens to have the IR Register map defined and the width of the the register.  'BYPASS' is prepopulated in the base class at last address in the IRLEN address map.

First inherit from the base class, , and after add all the other IR regiters using the _add_jtag_reg_ method.


    from cocotbext.jtag import JTAGDevice

    class J1JTAGDevice(JTAGDevice):
        def __init__(self, name='jtaglet1', idcode=0x53817905, ir_len=5):
            super().__init__(name, idcode, ir_len)
            self.add_jtag_reg("IDCODE", 32, 0x1e)
            self.add_jtag_reg('USERDATA', 32, 0x8)
            self.add_jtag_reg('USEROP', 8, 0x9)
            self.idle_delay = 6

* `add_jtag_reg(name, width, address)`: Add an IR register to `JTAGDevice`. _name_ is a string, _width_ is the DR shift width of the register and the address, which should be with in the range if the _ir_len_ of `JTAGDevice`

            
This results in a `JTAGDevice` that has 4 IR register defined:


    0x08: USERDATA[31:0] 
    0x09: USEROP[7:0] 
    0x1e: IDCODE[31:0] 
    0x1f: BYPASS[0:0] 


Multiple devices inside the JTAG chain:

    from cocotbext.jtag import JTAGDriver
    from cocotbext.jtag import JTAGBus

    class testbench:
        def __init__(self, dut):
            bus = JTAGBus(dut)
            self.jtag = JTAGDriver(bus)
            self.jtag.add_device(J1JTAGDevice())
            self.jtag.add_device(J2JTAGDevice())






