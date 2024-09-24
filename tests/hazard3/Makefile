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

VERILOG_INCLUDE_DIRS = \
	${PROJ_HOME}/tests/rtl/hazard3

EXT_VERILOG_SOURCES += \
    ${PROJ_HOME}/tests/rtl/cdc/sync_1bit.v \
    ${PROJ_HOME}/tests/rtl/uart/uart_regs.v \
    ${PROJ_HOME}/tests/rtl/uart/uart_mini.v \
    ${PROJ_HOME}/tests/rtl/busfabric/ahbl_to_apb.v \
    ${PROJ_HOME}/tests/rtl/busfabric/ahbl_splitter.v \
    ${PROJ_HOME}/tests/rtl/busfabric/apb_splitter.v \
    ${PROJ_HOME}/tests/rtl/mem/sram_sync_1r1w.v \
    ${PROJ_HOME}/tests/rtl/mem/ahb_sync_sram.v \
    ${PROJ_HOME}/tests/rtl/hazard3/debug/cdc/hazard3_reset_sync.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_core.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_cpu_1port.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_cpu_2port.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_alu.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_branchcmp.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_mul_fast.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_muldiv_seq.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_onehot_encode.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_onehot_priority.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_onehot_priority_dynamic.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_priority_encode.v \
    ${PROJ_HOME}/tests/rtl/hazard3/arith/hazard3_shift_barrel.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_csr.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_decode.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_frontend.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_instr_decompress.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_irq_ctrl.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_pmp.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_power_ctrl.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_regfile_1w2r.v \
    ${PROJ_HOME}/tests/rtl/hazard3/hazard3_triggers.v \
    ${PROJ_HOME}/tests/rtl/hazard3/debug/dm/hazard3_dm.v \
    ${PROJ_HOME}/tests/rtl/hazard3/debug/dtm/hazard3_jtag_dtm.v \
    ${PROJ_HOME}/tests/rtl/hazard3/debug/dtm/hazard3_jtag_dtm_core.v \
    ${PROJ_HOME}/tests/rtl/hazard3/debug/cdc/hazard3_apb_async_bridge.v \
    ${PROJ_HOME}/tests/rtl/hazard3/debug/cdc/hazard3_sync_1bit.v \
    ${PROJ_HOME}/tests/rtl/common/clkdiv_frac.v \
    ${PROJ_HOME}/tests/rtl/common/sync_fifo.v \
    ${PROJ_HOME}/tests/rtl/common/reset_sync.v \
    ${PROJ_HOME}/tests/rtl/common/onehot_mux.v \
    ${PROJ_HOME}/tests/rtl/common/hazard3_riscv_timer.v \

INT_VERILOG_SOURCES += \
    ${PROJ_HOME}/tests/rtl/common/top_soc.v \

COCOTB_SOURCES = \
    ./dut.sv


include ${PROJ_HOME}/rtlflo/cocotb_helper.mak
