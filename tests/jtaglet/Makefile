SIM?=icarus
TOPLEVEL_LANG=verilog
#XILINX_BASE=${HOME}/projects/XilinxUnisimLibrary
PROJ_HOME?=..

WORK_BASE?=../..

TOPLEVEL = dut
MODULE = test_dut

# XILINX_PART?=xc7a100tcsg324-1
# XILINX_REV?=2021.2
# ifneq (,$(wildcard ./makefile_synth.mak))
#     include ./makefile_synth.mak
# endif

# SIM_VERILOG_SOURCES += \
#     ${PROJ_HOME}/rtl/common/pixelasic.sv \
#     ${PROJ_HOME}/rtl/common/bambam_tile.sv 

INT_VERILOG_SOURCES += \
    ${PROJ_HOME}/jtaglet/ff_sync.v \
    ${PROJ_HOME}/jtaglet/jtag_reg.v \
    ${PROJ_HOME}/jtaglet/jtag_state_machine.v \
	${PROJ_HOME}/jtaglet.v

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
