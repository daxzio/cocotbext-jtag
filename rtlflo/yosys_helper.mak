# Use same top as vlint (TOPLEVEL from project Makefile, e.g. dut for hulk_top)
SYNTH_TOP ?= ${TOPLEVEL}

# Build Yosys flags from same DEFINES and VERILOG_INCLUDE_DIRS as vlint
ifdef DEFINES
	YOSYS_CMDS += $(addprefix -D, $(DEFINES))
endif
ifdef VERILOG_INCLUDE_DIRS
	YOSYS_CMDS += $(addprefix -I, $(VERILOG_INCLUDE_DIRS))
endif

# Same sources as vlint: EXT + INT + SIM
YOSYS_VERILOG_SOURCES ?= $(EXT_VERILOG_SOURCES) $(INT_VERILOG_SOURCES) $(SIM_VERILOG_SOURCES)

# Log file for parsing warnings and errors (use YSYNTH_LOG= to disable)
YSYNTH_LOG ?= ysynth.log

# Suppress specific warnings: -w "regex" demotes matching warnings to messages.
# Use -qq to suppress all warnings. Example: YOSYS_FLAGS='-w "Replacing memory"'
#YOSYS_FLAGS ?=
YOSYS_FLAGS += -w "Replacing memory"

# Synthesis check: same top and sources as vlint, verifies design elaborates and synthesizes
ysynth:
# ifneq ($(YSYNTH_LOG),)
	@yosys ${YOSYS_FLAGS} -p "\
		read_verilog -sv ${YOSYS_CMDS} ${YOSYS_VERILOG_SOURCES} ; \
		hierarchy -top ${TOPLEVEL} ; \
		synth ; \
		stat ; \
	" > $(YSYNTH_LOG) 2>&1; \
	echo "--- Warnings and errors ---"; \
	result=$$(grep -E "Warning|ERROR|Error" $(YSYNTH_LOG) | grep -v Suppressed); \
	echo "$$result"; \
	[ -n "$$result" ] && exit 1 || true
# else
# 	yosys ${YOSYS_FLAGS} -p "\
# 		read_verilog -sv ${YOSYS_CMDS} ${YOSYS_VERILOG_SOURCES} ; \
# 		hierarchy -top ${TOPLEVEL} ; \
# 		synth ; \
# 		stat ; \
# 	"
# endif

# Full Xilinx synthesis (produces EDIF)
yosys:
	yosys ${YOSYS_FLAGS} -p "\
		read_verilog -sv ${YOSYS_CMDS} ${YOSYS_VERILOG_SOURCES} ; \
		synth_xilinx -edif ${SYNTH_TOP}.edif -top ${SYNTH_TOP} ; \
	"
# 	yosys -p "\
# 		read_verilog -sv ${YOSYS_CMDS} ${VERILOG_DESIGN} ; \
# 		hierarchy -top ${SYNTH_TOP}; \
# 		proc; \
# 		flatten; \
# 		synth ; \
#         synth_xilinx -edif ${SYNTH_TOP}.edif ; \
# 		write_verilog ${SYNTH_TOP}_synth.v ; \
# 	"

clean::
	rm -rf ${SYNTH_TOP}_synth.v ${SYNTH_TOP}.edif $(YSYNTH_LOG)
