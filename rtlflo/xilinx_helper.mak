XILINX_REV?=2021.2
XILINX_PART?=xc7a100tcsg324-1
CDSLIB?=./cds_${SIM}.lib
COMPILE_LIBS?=../../libs
RTLFLO_PATH?=../rtlflo
RTLFLO_PATH:=$(abspath ${RTLFLO_PATH})

SYNTH_TOP?=${TOPLEVEL}
BUILD_NAME?=${SYNTH_TOP}


XILINX_LIB=${COMPILE_LIBS}/${SIM}/xilinx
ifneq ($(XILINX_VIVADO),)
XILINX_BASE?=${XILINX_VIVADO}/data
XILINX_LIB=${COMPILE_LIBS}/${SIM}/xilinx-${XILINX_REV}
endif

ifeq ($(SIM),xcelium)
CADENCE_VLOG?=xmvlog
CADENCE_VHDL?=xmvhdl
else
CADENCE_VLOG?=ncvlog
CADENCE_VHDL?=ncvhdl
endif
# DEFINES += COCOTB_IUS=1

ifneq (${USE_CDS},)
    ifeq ($(SIM),xcelium)
		COMPILE_ARGS += -cdslib ${CDSLIB}
	else ifeq ($(SIM),ius)
		COMPILE_ARGS += -cdslib ${CDSLIB}
    else ifeq ($(SIM),verilator)
# 	    COMPILE_ARGS += --top-module glbl
# 		VERILOG_SOURCES += \
# 			${XILINX_BASE}/verilog/src/glbl.v
# 	    VERILOG_SOURCES += ${UNISIMS}
    endif
endif

ifneq (${XILINX_BASE},)
	UNISIMS_VER_CNT=`grep -s unisims_ver ${CDSLIB} | wc -l`
	UNISIMS_VHDL_CNT=`grep -s unisim ${CDSLIB} | wc -l`

#     UNISIMS = \
# 	    ${XILINX_BASE}/verilog/src/unisims/FDRE.v \
# 	    ${XILINX_BASE}/verilog/src/unisims/FDSE.v \
# 	    ${XILINX_BASE}/verilog/src/unisims/GND.v \
# 	    ${XILINX_BASE}/verilog/src/unisims/MMCME2_ADV.v

    ifeq ($(SIM), icarus)
        ifneq ($(XILINX_SIM_SOURCES),)
			COMPILE_ARGS += -y${XILINX_BASE}/verilog/src/unisims
			COMPILE_ARGS += -s glbl
		endif
	else ifeq ($(SIM),xcelium)
		COMPILE_ARGS += -top glbl
		VERILOG_SOURCES += \
			${XILINX_BASE}/verilog/src/glbl.v
	else ifeq ($(SIM),ius)
        ifneq (${VERILOG_SOURCES},)
		    COMPILE_ARGS += -top glbl
		    VERILOG_SOURCES += \
			    ${XILINX_BASE}/verilog/src/glbl.v
		endif
    else ifeq ($(SIM),verilator)
# 	    COMPILE_ARGS += --top-module glbl
# 		VERILOG_SOURCES += \
# 			${XILINX_BASE}/verilog/src/glbl.v
# 	    VERILOG_SOURCES += ${UNISIMS}
    endif

endif

default: sim

xilinx_cdslib:
	@if [ "${UNISIMS_VHDL_CNT}" -eq "0" ]; then \
		mkdir -p ${XILINX_LIB}/unisim ; \
		mkdir -p ${XILINX_LIB}/secureip ; \
		echo "DEFINE unisim ${XILINX_LIB}/unisim" >> ${CDSLIB} ; \
		echo "DEFINE secureip ${XILINX_LIB}/secureip" >> ${CDSLIB} ; \
	fi
	@if [ "${UNISIMS_VER_CNT}" -eq "0" ]; then \
		mkdir -p ${XILINX_LIB}/unisims_ver ; \
		echo "DEFINE unisims_ver ${XILINX_LIB}/unisims_ver" >> ${CDSLIB} ; \
	fi


${XILINX_LIB}/unisims_ver: ${CDSLIB} xilinx_cdslib
	${CADENCE_VLOG} -MESSAGES -NOLOG -64bit -CDSLIB ${CDSLIB} -WORK unisims_ver ${XILINX_BASE}/verilog/src/unisims/*.v
	${CADENCE_VLOG} -MESSAGES -NOLOG -64bit -CDSLIB ${CDSLIB} -SV -WORK unisims_ver ${XILINX_BASE}/verilog/src/unisims/*.sv
	@if [ -d "${XILINX_BASE}/secureip" ]; then \
		${CADENCE_VLOG} -MESSAGES -NOLOG -64bit -CDSLIB ${CDSLIB} -WORK unisims_ver ${XILINX_BASE}/secureip/*/*.vp; \
	fi

${XILINX_LIB}/unisim: ${CDSLIB} xilinx_cdslib
	@if [ -d "${XILINX_BASE}/vhdl" ]; then \
		${CADENCE_VHDL} -MESSAGES -NOLOG -64bit -v93 -CDSLIB ${CDSLIB} -WORK unisim \
			${XILINX_BASE}/vhdl/src/unisims/unisim_VPKG.vhd \
			${XILINX_BASE}/vhdl/src/unisims/unisim_VCOMP.vhd \
			${XILINX_BASE}/vhdl/src/unisims/primitive/*.vhd ; \
		${CADENCE_VHDL} -MESSAGES -NOLOG -64bit -v93 -CDSLIB ${CDSLIB} -WORK secureip \
			${XILINX_BASE}/vhdl/src/unisims/secureip/*.vhd ;\
	fi

xilinx_lib: | ${XILINX_LIB}/unisims_ver ${XILINX_LIB}/unisim

xilinx_library:
	mkdir -p ${COMPILE_LIBS}
ifeq ($(SIM),ius)
	${MAKE} xilinx_lib
else ifeq ($(SIM),xcelium)
	${MAKE} xilinx_lib
endif

xilinx_library_clean:
	@rm -rf ${XILINX_LIB}
	@sed -in '/unisim/d' ${CDSLIB} || true
	@sed -in '/secureip/d' ${CDSLIB} || true

cdslib:: xilinx_cdslib

all_libs:: xilinx_library

all_libs_clean:: xilinx_library_clean

XILINX_GENERICS += \
    ${GENERICS} \
 	G_FPGA_VERSION=32'h25031800 \

XILINX_DEFINES += \
    ${DEFINES} \

FPGA_DESIGN:=\
    ${XILINX_SYNTH_SOURCES} \
    ${MEM_FILE_SOURCES} \
    ${INT_VERILOG_SOURCES} \
    ${EXT_VERILOG_SOURCES} \
    ${INT_VHDL_SOURCES} \
    ${EXT_VHDL_SOURCES}

XILINX_PRE_CUSTOM += \
    set_msg_config -id {Synth 8-324} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Synth 8-327} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Synth 8-689} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Synth 8-6901} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Synth 8-6841} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Synth 8-7023} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Synth 8-7071} -new_severity {CRITICAL WARNING}; \
    set_msg_config -id {Designutils 20-1280} -new_severity {WARNING}; \
    set_msg_config -id {Designutils 20-1281} -new_severity {WARNING}; \
    set_msg_config -id {Place 30-73} -new_severity {WARNING}; \
    set_msg_config -suppress -id {DRC PDRC-34}; \

XILINX_PRE_CUSTOM += \
    add_files -fileset utils_1 -norecurse ${RTLFLO_PATH}/post_bitstream.tcl; \
    add_files -fileset utils_1 -norecurse ${RTLFLO_PATH}/pre_synth.tcl; \
    set_property STEPS.SYNTH_DESIGN.TCL.PRE [ get_files ${RTLFLO_PATH}/pre_synth.tcl -of [get_fileset utils_1] ] [get_runs synth_1];\
    set_property STEPS.WRITE_BITSTREAM.TCL.POST [ get_files ${RTLFLO_PATH}/post_bitstream.tcl -of [get_fileset utils_1] ] [get_runs impl_1];\

XILINX_POST_CUSTOM += \
    set_property source_mgmt_mode All [current_project]; \
    update_compile_order -fileset sources_1; \

vivado_build:
	@ export XILINX_PART="${XILINX_PART}" ; \
	export XILINX_CONSTRAINTS="${XILINX_CONSTRAINTS}" ; \
	export XILINX_PRE_CUSTOM='${XILINX_PRE_CUSTOM}' ; \
	export XILINX_POST_CUSTOM='${XILINX_POST_CUSTOM}' ; \
	export SYNTH_TOP=${SYNTH_TOP} ; \
	export BUILD_NAME=${BUILD_NAME} ; \
	export VERILOG_INCLUDE_DIRS="${VERILOG_INCLUDE_DIRS}" ; \
	export GENERICS="${XILINX_GENERICS}" ; \
	export DEFINES="${XILINX_DEFINES}" ; \
	export FPGA_DESIGN="${FPGA_DESIGN}" ; \
		${RTLFLO_PATH}/vivado_helper.py

vivado_clean:
	rm -rf build-*/ vivado* *.err .Xil/
