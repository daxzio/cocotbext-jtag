TOPLEVEL_LANG?=verilog
TOPLEVEL?=dut
MODULE?=test_dut

COCOTB_RESOLVE_X?=ZEROS
export COCOTB_RESOLVE_X

ifneq (,$(wildcard ./makefile_synth.mak))
default: vivado_build
SIM:=icarus
else
default: sim
endif

include $(shell cocotb-config --makefiles)/Makefile.sim
include ${WORK_BASE}/rtlflo/xilinx_helper.mak
include ${WORK_BASE}/rtlflo/verible_helper.mak
include ${WORK_BASE}/rtlflo/git_helper.mak


# Process generics
ifeq ($(TOPLEVEL_LANG),verilog)
	ifeq ($(SIM), icarus)
	    COMPILE_ARGS += $(addprefix -P${TOPLEVEL}., $(GENERICS))
	else ifneq ($(filter $(SIM),questa modelsim riviera activehdl),)
	    SIM_ARGS += $(addprefix -g, $(GENERICS))
	else ifeq ($(SIM),vcs)
	    COMPILE_ARGS += $(addprefix -pvalue+/, $(GENERICS))
	else ifeq ($(SIM),verilator)
	    COMPILE_ARGS += $(addprefix -G, $(GENERICS))
	else ifneq ($(filter $(SIM),ius xcelium),)
	    EXTRA_ARGS += $(addprefix -defparam ${TOPLEVEL}., $(GENERICS))
	endif
else ifeq ($(TOPLEVEL_LANG),vhdl)
    ifneq ($(filter $(SIM),ghdl questa modelsim riviera activehdl),)
        # ghdl, questa, and aldec all use SIM_ARGS with '-g' for setting generics
        SIM_ARGS += $(addprefix -g, $(GENERICS))
    else ifneq ($(filter $(SIM),ius xcelium),)
        SIM_ARGS += $(addprefix -generic \"${TOPLEVEL}:, $(addsuffix \", $(subst =,=>, $(GENERICS))))
    endif
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

# Process defines
ifeq ($(TOPLEVEL_LANG),verilog)
	ifeq ($(SIM), icarus)
	    COMPILE_ARGS += $(addprefix -D , $(DEFINES))
	else ifneq ($(filter $(SIM),questa modelsim riviera activehdl),)
	    #SIM_ARGS += $(addprefix -g, $(GENERICS))
	else ifeq ($(SIM),vcs)
	    #COMPILE_ARGS += $(addprefix -pvalue+/, $(GENERICS))
	else ifeq ($(SIM),verilator)
	    #COMPILE_ARGS += $(addprefix -G, $(GENERICS))
	else ifneq ($(filter $(SIM),ius xcelium),)
	    EXTRA_ARGS += $(addprefix -define , $(DEFINES))
	endif
else ifeq ($(TOPLEVEL_LANG),vhdl)
    ifneq ($(filter $(SIM),ghdl questa modelsim riviera activehdl),)
        #SIM_ARGS += $(addprefix -g, $(GENERICS))
    else ifneq ($(filter $(SIM),ius xcelium),)
        #SIM_ARGS += $(addprefix -generic \"${TOPLEVEL}:, $(addsuffix \", $(subst =,=>, $(GENERICS))))
    endif
else
    $(error "A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

ifeq ($(TOPLEVEL_LANG),verilog)
	ifeq ($(SIM), icarus)
	    COMPILE_ARGS += -D COCOTB_ICARUS=1
		WAVES=1
	else ifeq ($(SIM), ius)
		COMPILE_ARGS += -disable_sem2009
		COMPILE_ARGS += -sv
		COMPILE_ARGS += -top ${TOPLEVEL}
	else ifeq ($(SIM),xcelium)
		COMPILE_ARGS += -disable_sem2009
		COMPILE_ARGS += -sv
		COMPILE_ARGS += -top ${TOPLEVEL}
	else ifeq ($(SIM),verilator)
	    COMPILE_ARGS += -DCOCOTB_VERILATOR=1
		COMPILE_ARGS += --no-timing -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-STMTDLY
		EXTRA_ARGS += --trace-fst --trace-structs
		#SIM_ARGS += --trace 
	endif
endif

${CDSLIB}:
	echo "include \$${INCISIVE_HOME}/tools.lnx86/inca/files/cds.lib" > ${CDSLIB}

cdslib:: ${CDSLIB}

all_libs_clean::
	@rm -rf ${CDSLIB}

waves:
ifeq ($(SIM), icarus)
	gtkwave dut.vcd &
else ifeq ($(SIM), ius)
	simvision -waves waves.shm &
else ifeq ($(SIM),verilator)
	gtkwave dump.fst &
endif

clean::
	rm -rf __pycache__/ .simvision/ .Xil/ results.xml *.trn *.dsn vivado* *.vcd *.out irun* simvision* xrun* .bpad/ waves.shm/ *.err INCA_libs/ *.fst* ncvlog.log

