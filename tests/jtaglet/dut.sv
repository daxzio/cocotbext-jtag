module dut #(
      parameter integer IR_LEN       = 4
    , parameter ID_PARTVER   = 4'h1
    , parameter ID_PARTNUM   = 16'hbeef
    , parameter ID_MANF      = 11'h035
    , parameter integer USERDATA_LEN = 32
    , parameter integer USEROP_LEN   = 8
) (
      input                         tck
    , input                         tms
    , input                         tdi
    , output reg                    tdo
    , input                         trst
    , input      [USERDATA_LEN-1:0] userData_in
    , output     [USERDATA_LEN-1:0] userData_out
    , output     [  USEROP_LEN-1:0] userOp
    , output                        userOp_ready
);


    jtaglet #(
          .IR_LEN    (IR_LEN)
        , .ID_PARTVER(ID_PARTVER)
        , .ID_PARTNUM(ID_PARTNUM)
        , .ID_MANF   (ID_MANF)
    ) i_jtaglet (
        .*
        , .userData_in (userData_in)
        , .userData_out(userData_out)
        , .userOp      (userOp)
        , .userOp_ready(userOp_ready)
    );

    `ifdef COCOTB_SIM
//`ifdef COCOTB_ICARUS
    initial begin
        $dumpfile("dut.vcd");
        $dumpvars(0, dut);
        /* verilator lint_off STMTDLY */
        #1;
        /* verilator lint_on STMTDLY */
    end
`endif

endmodule

