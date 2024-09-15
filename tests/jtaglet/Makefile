SIM?=icarus
TOPLEVEL_LANG=verilog
#XILINX_BASE=${HOME}/projects/XilinxUnisimLibrary
PROJ_HOME?=../..

WORK_BASE?=../..

TOPLEVEL = dut
MODULE = test_dut

INT_VERILOG_SOURCES += \
    ${PROJ_HOME}/tests/rtl/jtaglet/ff_sync.v \
    ${PROJ_HOME}/tests/rtl/jtaglet/jtag_reg.v \
    ${PROJ_HOME}/tests/rtl/jtaglet/jtag_state_machine.v \
	${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.v

COCOTB_SOURCES = \
    ./dut.sv

include ${PROJ_HOME}/rtlflo/cocotb_helper.mak
