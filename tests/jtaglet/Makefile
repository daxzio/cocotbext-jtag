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

# VERILOG_DESIGN += \
#     ${INT_VERILOG_SOURCES} \
#     ${SIM_VERILOG_SOURCES} \
#     ${EXT_VERILOG_SOURCES} \
#     ${XILINX_SIM_SOURCES}
# 
# VERILOG_SOURCES = \
#     ${VERILOG_DESIGN} \
#     ${COCOTB_SOURCES}

include ${PROJ_HOME}/rtlflo/cocotb_helper.mak
