#!/usr/bin/env python
import os
import re
from pyfpga.vivado import Vivado


class vivado_helper:
    def __init__(self):
        self.cwd = os.getcwd()
        self.xilinx_rev = os.environ["XILINX_REV"]
        self.part = os.environ["XILINX_PART"]
        self.top = os.environ["SYNTH_TOP"]
        self.buildname = os.environ["BUILD_NAME"]
        self.build_dir = f"{self.cwd}/build-{self.xilinx_rev}"

        self.vlog_files = []
        self.slog_files = []
        self.vhdl_files = []
        self.xcix_files = []
        if "FPGA_DESIGN" in os.environ:
            for x in os.environ["FPGA_DESIGN"].split():
                if "" == x:
                    continue
                file = x.rstrip().lstrip()
                _, ext = os.path.splitext(file)
                if ".svh" == ext:
                    raise Exception(
                        'Do not add svh files to filelist, make sure it is included:\n`include "avsbus_pkg.svh"\nimport avsbus_pkg::*;'
                    )
                if ".sv" == ext:
                    self.slog_files.append(file)
                elif ".vhd" == ext or ".vhdl" == ext:
                    self.vhdl_files.append(file)
                elif ".xci" == ext or ".xcix" == ext:
                    self.xcix_files.append(file)
                else:
                    self.vlog_files.append(file)

        self.constraints = []
        if "XILINX_CONSTRAINTS" in os.environ:
            for x in os.environ["XILINX_CONSTRAINTS"].split():
                if "" == x:
                    continue
                self.constraints.append(x.rstrip().lstrip())

        self.pre_customs = []
        if "XILINX_PRE_CUSTOM" in os.environ:
            for x in os.environ["XILINX_PRE_CUSTOM"].split(";"):
                self.pre_customs.append(x.rstrip().lstrip())

        self.post_customs = []
        if "XILINX_POST_CUSTOM" in os.environ:
            for x in os.environ["XILINX_POST_CUSTOM"].split(";"):
                self.post_customs.append(x.rstrip().lstrip())

        self.include_dirs = []
        if "VERILOG_INCLUDE_DIRS" in os.environ:
            for x in os.environ["VERILOG_INCLUDE_DIRS"].split():
                if "" == x:
                    continue
                self.include_dirs.append(x.rstrip().lstrip())

        self.generics = os.environ["GENERICS"].rstrip().split()
        self.defines = os.environ["DEFINES"].rstrip().split()

        self.prj = Vivado(self.buildname, odir=self.build_dir)
        self.prj.set_debug()

    def create_project(self):
        #         self.prj.clean()
        self.prj.set_part(self.part)

        for pre_custom in self.pre_customs:
            self.prj.add_hook("precfg", pre_custom)

        for generic in self.generics:
            g = generic.split("=")
            self.prj.add_param(g[0], g[1])

        for define in self.defines:
            if re.search("=", define):
                d = define.split("=")
                self.prj.add_define(d[0], d[1])
            else:
                self.prj.add_define(define, 0)

        for constraint in self.constraints:
            c = constraint.split(",")
            self.prj.add_cons(c[0])
            if len(c) > 1:
                self.prj.add_hook(
                    f"set_property SCOPED_TO_REF {c[1]} [get_files {c[0]}]"
                )

        for include_dir in self.include_dirs:
            self.prj.add_include(include_dir)

        for file in self.vlog_files:
            self.prj.add_vlog(file)
        for file in self.slog_files:
            self.prj.add_slog(file)
        for file in self.vhdl_files:
            self.prj.add_vhdl(file)
        for file in self.xcix_files:
            self.prj.add_vlog(file)
        self.prj.set_top(self.top)
        #         self.prj.add_define("FPGA", 1)
        #         self.prj.add_hook('postcfg', "set_property source_mgmt_mode All [current_project]")
        #         self.prj.add_hook('postcfg', "update_compile_order -fileset sources_1")
        #         self.prj.generate("prj")
        for custom in self.post_customs:
            self.prj.add_hook("postcfg", custom)

        self.prj.make(last="cfg")

    def generate_bitstream(self):
        self.prj.generate("bit")


#     def reportBitfileName(self):
#         print(f"{self.bitstream}")
#
#     def reportProductId(self):
#         return f"{self.product_id:04x}"
#
#     def reportVersionId(self):
#         return f"{self.version_id:08x}"
#
#     def reportDate(self):
# #         self.date_str = time.ctime(os.path.getctime(self.bitstream))
# #         self.date_str = datetime.datetime.strptime(self.date_str, "%c")
# #         self.unique_id = self.date_str.strftime('%y%m%d')
# #         #xx = time.strftime("%y", self.date_str)
#         print(f"{self.unique_id}")
#         #print(f"{self.product_id}")


def main(stage="all"):
    v = vivado_helper()
    v.create_project()


#     v.generate_bitstream()

if __name__ == "__main__":

    stage = "all"
    #     if 2 == len(sys.argv):
    #         stage = sys.argv[1]
    #     if not stage in ["all", "build", "synth", "run", "bitfile", "date", "date_fpga"]:
    #         raise Exception(f"Unknown stage: {stage}")
    main(stage)
