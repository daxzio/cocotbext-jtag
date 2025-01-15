SYNTH_TOP?=top

yosys:
	yosys -p "\
		read_verilog -sv ${VERILOG_DESIGN}; \
		hierarchy -top ${SYNTH_TOP}; \
		proc; \
		flatten; \
		synth ; \
		write_verilog synth_yosys.v; \
	"

clean::
	rm -rf synth_yosys.v
