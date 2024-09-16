SIM?=icarus
TOPLEVEL_LANG=verilog
#XILINX_BASE=${HOME}/projects/XilinxUnisimLibrary
PROJ_HOME?=../..

WORK_BASE?=../..

TOPLEVEL = dut
MODULE = test_dut

# XILINX_PART?=xc7a100tcsg324-1
# XILINX_REV?=2021.2
# ifneq (,$(wildcard ./makefile_synth.mak))
#     include ./makefile_synth.mak
# endif

# SIM_VERILOG_SOURCES += \

INT_VERILOG_SOURCES += \
    ${PROJ_HOME}/tests/rtl/jtaglet/ff_sync.v \
    ${PROJ_HOME}/tests/rtl/jtaglet/jtag_reg.v \
    ${PROJ_HOME}/tests/rtl/jtaglet/jtag_state_machine.v \
	${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.v

COCOTB_SOURCES = \
    ./dut.sv


include ${PROJ_HOME}/rtlflo/cocotb_helper.mak
