# svlint: SystemVerilog linter (same top and sources as vlint)
# Requires .svlint.toml config; run 'svlint --example' to create one.
# Uses filelist for +incdir, +define, and source files.

SVLINT_FL ?= svlint.fl
SVLINT_VERILOG_SOURCES ?= $(EXT_VERILOG_SOURCES) $(INT_VERILOG_SOURCES) $(SIM_VERILOG_SOURCES)

svlint: $(SVLINT_FL)
	svlint -f $(SVLINT_FL)

# Generate filelist from VERILOG_INCLUDE_DIRS, DEFINES, and sources
$(SVLINT_FL):
	@rm -f $(SVLINT_FL)
	@$(foreach inc, $(VERILOG_INCLUDE_DIRS), echo "+incdir+$(inc)" >> $(SVLINT_FL);)
	@$(foreach def, $(DEFINES), echo "+define+$(def)" >> $(SVLINT_FL);)
	@for f in $(SVLINT_VERILOG_SOURCES); do echo "$$f" >> $(SVLINT_FL); done

clean::
	rm -f $(SVLINT_FL)
