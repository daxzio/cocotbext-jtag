# ifdef VERILOG_INCLUDE_DIRS
#   VINCLUDE_ARGS += $(addprefix +incdir+, $(VERILOG_INCLUDE_DIRS))
# endif

vlint:
	verilator --lint-only \
		$(addprefix +incdir+, $(VERILOG_INCLUDE_DIRS)) \
		$(addprefix -D, $(DEFINES)) \
    	${IGNORE_ARGS} \
		$(EXT_VERILOG_SOURCES) $(INT_VERILOG_SOURCES) $(SIM_VERILOG_SOURCES) \
        --top-module ${TOPLEVEL}
