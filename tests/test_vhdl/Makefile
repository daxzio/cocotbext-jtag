SIM?=ghdl
TOPLEVEL_LANG=vhdl
#XILINX_BASE=${HOME}/projects/XilinxUnisimLibrary
PROJ_HOME?=../..

WORK_BASE?=../..

TOPLEVEL = dut
MODULE = test_dut

VHDL_OUTPUT := ${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.vhd

CONV_VERILOG_SOURCES += \
    ${PROJ_HOME}/tests/rtl/jtaglet/ff_sync.v \
    ${PROJ_HOME}/tests/rtl/jtaglet/jtag_reg.v \
    ${PROJ_HOME}/tests/rtl/jtaglet/jtag_state_machine.v \
	${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.v

CONV_GENERICS+=\
	IR_LEN=5 \
	ID_PARTVER=4'h5 \
	ID_PARTNUM=16'h3817 \
	ID_MANF=11'h482

CONV_TOPLEVEL?=jtaglet

VHDL_SOURCES+=\
	${VHDL_OUTPUT} \
#     ${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.vhd \


COCOTB_SOURCES = \
    ./dut.vhd

default: vlog2vhdl sim

# ${VHDL_OUTPUT}: vlog2vhdl

include ${PROJ_HOME}/rtlflo/cocotb_helper.mak
