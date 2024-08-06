module dut  #(
    parameter IR_LEN = 4
//    , parameter ID_PARTVER = 4'h0
//    , parameter ID_PARTNUM = 16'h0000
//    , parameter ID_MANF = 11'h000
//    , parameter USERDATA_LEN = 32
//    , parameter USEROP_LEN = 8
    )(
      input tck
    , input tms
    , input tdi
    , output reg tdo
    , input trst
);


    jtaglet # (
        .IR_LEN    (IR_LEN)
//         , .ID_PARTVER   (ID_PARTVER)
    )
    i_jtaglet (
        .*
        , .userData_in (0)
        , .userData_out ( )
        , .userOp ( )
        , .userOp_ready ( )
    );
    
    //`ifdef COCOTB_SIM
    `ifdef COCOTB_ICARUS
    initial begin
        $dumpfile ("dut.vcd");
        $dumpvars (0, dut);
        /* verilator lint_off STMTDLY */
        #1;
        /* verilator lint_on STMTDLY */
    end
    `endif    

endmodule

