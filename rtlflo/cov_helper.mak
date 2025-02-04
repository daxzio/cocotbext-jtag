COV_ARGS += $(addprefix -P "${CONV_TOPLEVEL}., $(addsuffix ", $(CONV_GENERICS)))
COV_ARGS += -pdebug=1

vlog2vhdl:
	iverilog \
    	-g2012 \
    	-t vhdl \
		${COV_ARGS} \
    	${CONV_VERILOG_SOURCES} \
    	-o ${VHDL_OUTPUT}
