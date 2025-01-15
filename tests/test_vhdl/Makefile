SIM?=ghdl
TOPLEVEL_LANG=vhdl
#XILINX_BASE=${HOME}/projects/XilinxUnisimLibrary
PROJ_HOME?=../..

WORK_BASE?=../..

TOPLEVEL = dut
MODULE = test_dut

VHDL_SOURCES+=\
	../rtl/jtaglet/jtaglet.vhd \

# XILINX_PART?=xc7a100tcsg324-1
# XILINX_REV?=2021.2
# ifneq (,$(wildcard ./makefile_synth.mak))
#     include ./makefile_synth.mak
# endif


# INT_VERILOG_SOURCES += \
#     ${PROJ_HOME}/tests/rtl/jtaglet/ff_sync.v \
#     ${PROJ_HOME}/tests/rtl/jtaglet/jtag_reg.v \
#     ${PROJ_HOME}/tests/rtl/jtaglet/jtag_state_machine.v \
# 	${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.v

COCOTB_SOURCES = \
    ./dut.vhd

vlog2vhdl:
	iverilog \
    	-g2012 \
    	-t vhdl \
    	-pdebug=1 \
    	-o ${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.vhd \
    	${PROJ_HOME}/tests/rtl/jtaglet/jtag_state_machine.v ${PROJ_HOME}/tests/rtl/jtaglet/jtag_reg.v ${PROJ_HOME}/tests/rtl/jtaglet/ff_sync.v ${PROJ_HOME}/tests/rtl/jtaglet/jtaglet.v \
		-P  jtaglet.IR_LEN='5' \
		-P "jtaglet.ID_PARTVER=4'h5" \
		-P "jtaglet.ID_PARTNUM=16'h3817" \
		-P "jtaglet.ID_MANF=11'h482" 


include ${PROJ_HOME}/rtlflo/cocotb_helper.mak
