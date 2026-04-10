TOPLEVEL_LANG?=verilog
TOPLEVEL?=dut
COCOTB_TEST_MODULES?=test_dut
RTLFLO_PATH?=../rtlflo
RTLFLO_PATH:=$(abspath ${RTLFLO_PATH})

WAVES?=0

ifneq (,$(wildcard ./makefile_synth.mak))
default: vivado_build
SIM?=icarus
else
default: sim
endif

include ${RTLFLO_PATH}/xilinx_helper.mak
# Build VERILOG_SOURCES before including Makefile.sim so dependencies work
# strip: empty *_VERILOG_SOURCES still leave spaces between words; GHDL skips sim if VERILOG_SOURCES is non-empty
VERILOG_DESIGN ?= $(strip $(EXT_VERILOG_SOURCES) $(INT_VERILOG_SOURCES) $(SIM_VERILOG_SOURCES) $(XILINX_SIM_SOURCES))

VERILOG_SOURCES += $(VERILOG_DESIGN)

ifneq ($(strip $(INT_VHDL_SOURCES)$(EXT_VHDL_SOURCES)),)
VHDL_SOURCES += $(INT_VHDL_SOURCES) $(EXT_VHDL_SOURCES)
endif

include $(shell cocotb-config --makefiles)/Makefile.sim
include ${RTLFLO_PATH}/verilator_helper.mak
include ${RTLFLO_PATH}/svlint_helper.mak
include ${RTLFLO_PATH}/yosys_helper.mak
include ${RTLFLO_PATH}/verible_helper.mak
include ${RTLFLO_PATH}/git_helper.mak

# DEFINES += COCOTB_RUNNING=1
export COCOTB_RUNNING
ifeq ($(TOPLEVEL_LANG),verilog)
	ifeq ($(SIM), icarus)
        DEFINES += COCOTB_ICARUS=1
        SIM_BUILD:=sim_build_icarus
	else ifeq ($(SIM), ius)
        DEFINES += COCOTB_CADENCE=1
        DEFINES += COCOTB_IUS=1
		COMPILE_ARGS += -disable_sem2009
		COMPILE_ARGS += -sv
		COMPILE_ARGS += -top ${TOPLEVEL}
	else ifeq ($(SIM),xcelium)
        DEFINES += COCOTB_CADENCE=1
        DEFINES += COCOTB_XCELIUM=1
		COMPILE_ARGS += -disable_sem2009
		COMPILE_ARGS += -sv
# 		COMPILE_ARGS += -top ${TOPLEVEL}
        SIM_BUILD:=sim_build_xcelium
	else ifeq ($(SIM),verilator)
        #DEFINES += COCOTB_VERILATOR=1
		COMPILE_ARGS += --no-timing
		COMPILE_ARGS += --decorations none
# 		COMPILE_ARGS += OPT_FAST="-O0"
		COMPILE_ARGS += --compiler clang
	    COMPILE_ARGS += ${IGNORE_ARGS}
        SIM_BUILD:=sim_build_verilator
	else ifneq ($(filter $(SIM),questa modelsim ),)
        SIM_BUILD:=sim_build_questa
	endif
endif

ifeq ($(WAVES),1)
    #DEFINES += COCOTB_WAVES=1
	ifeq ($(SIM),verilator)
		COCOTB_PLUSARGS += --trace
		EXTRA_ARGS += --trace # vcd format
		EXTRA_ARGS += --trace-fst
		EXTRA_ARGS += --trace-structs
	else ifeq ($(SIM),xcelium)
		SIM_ARGS += -access +r
		SIM_ARGS += -input waves.tcl
	endif
endif


# Process generics
ifneq ($(filter $(SIM),questa modelsim),)
    SIM_ARGS += $(addprefix -g, $(GENERICS))
endif
ifeq ($(TOPLEVEL_LANG),verilog)
	ifeq ($(SIM), icarus)
        COMPILE_ARGS += $(addprefix -P${TOPLEVEL}., $(addsuffix ', $(subst =,=', $(GENERICS))))
	else ifneq ($(filter $(SIM),questa modelsim riviera activehdl),)
	    SIM_ARGS += $(addprefix -g, $(GENERICS))
	else ifeq ($(SIM),vcs)
	    COMPILE_ARGS += $(addprefix -pvalue+/, $(GENERICS))
	else ifeq ($(SIM),verilator)
	    COMPILE_ARGS += $(addprefix -G, $(addsuffix ', $(subst =,=', $(GENERICS))))
	else ifeq ($(SIM),ius)
	    EXTRA_ARGS += $(addprefix -defparam ${TOPLEVEL}., $(GENERICS))
	else ifeq ($(SIM),xcelium)
	    # xrun only pass numerics, string are not working
        EXTRA_ARGS += $(addprefix -defparam ${TOPLEVEL}., $(GENERICS))
	endif
else ifeq ($(TOPLEVEL_LANG),vhdl)
    ifneq ($(filter $(SIM),ghdl riviera activehdl),)
        # ghdl, questa, and aldec all use SIM_ARGS with '-g' for setting generics
        SIM_ARGS += $(addprefix -g, $(GENERICS))
    else ifneq ($(filter $(SIM),ius xcelium),)
        SIM_ARGS += $(addprefix -generic \"${TOPLEVEL}:, $(addsuffix \", $(subst =,=>, $(GENERICS))))
    endif
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

# Process defines
ifneq ($(filter $(SIM),questa modelsim),)
    #SIM_ARGS += $(addprefix -g, $(GENERICS))
endif
ifeq ($(TOPLEVEL_LANG),verilog)
	ifeq ($(SIM), icarus)
	    COMPILE_ARGS += $(addprefix -D , $(DEFINES))
	else ifneq ($(filter $(SIM),questa modelsim riviera activehdl),)
	    #SIM_ARGS += $(addprefix -g, $(GENERICS))
	else ifeq ($(SIM),vcs)
	    #COMPILE_ARGS += $(addprefix -pvalue+/, $(GENERICS))
	else ifeq ($(SIM),verilator)
	    EXTRA_ARGS += $(addprefix -D, $(DEFINES))
	else ifneq ($(filter $(SIM),ius xcelium),)
	    EXTRA_ARGS += $(addprefix -define , $(DEFINES))
	endif
else ifeq ($(TOPLEVEL_LANG),vhdl)
    ifneq ($(filter $(SIM),ghdl riviera activehdl),)
        #SIM_ARGS += $(addprefix -g, $(GENERICS))
    else ifneq ($(filter $(SIM),ius xcelium),)
        #SIM_ARGS += $(addprefix -generic \"${TOPLEVEL}:, $(addsuffix \", $(subst =,=>, $(GENERICS))))
    endif
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

ifeq ($(TOPLEVEL_LANG),verilog)
	VERILOG_SOURCES+=\
		${COCOTB_SOURCES}
else
	VHDL_SOURCES+=\
		${COCOTB_SOURCES}
endif

${CDSLIB}:
	echo "include \$${INCISIVE_HOME}/tools.lnx86/inca/files/cds.lib" > ${CDSLIB}

cdslib:: ${CDSLIB}

all_libs_clean::
	@rm -rf ${CDSLIB}

waves:
ifeq ($(SIM), icarus)
# 	gtkwave dut.vcd &
	gtkwave ${SIM_BUILD}/*.fst &
else ifeq ($(SIM), ius)
	simvision -waves waves.shm &
else ifeq ($(SIM),verilator)
	gtkwave dump.fst &
endif

# .PHONY: retest
retest:
	@rm -f results.xml
	@$(MAKE) regression SIM=$(SIM)


clean::
	rm -rf __pycache__/ .simvision/ .Xil/ results.xml *.trn *.dsn vivado* *.vcd *.out irun* simvision* xrun* .bpad/ waves.shm/ *.err INCA_libs/ *.fst* ncvlog.log
	rm -rf sim_build ${SIM_BUILD}
	rm -rf qrun* qwave.db transcript design.bin
