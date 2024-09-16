module dut (
      input      tck
    , input      tms
    , input      tdi
    , output reg tdo
    , input      trst
    //     , input rst
    //     , input gck
);

    localparam integer G_NUM_JTAG = 1;
    logic [G_NUM_JTAG-1:0] w_td;

    logic                  w_trst;

    logic [          31:0] d_userData[G_NUM_JTAG-1:0];
    logic [          31:0] f_userData[G_NUM_JTAG-1:0];

    //     assign f_userData = 32'he6712945;

    assign w_trst = trst;
    //     assign w_trst = rst;

    always @(posedge tck or negedge w_trst) begin
        if (!w_trst) begin
            f_userData[0] = 32'he6712945;
        end else begin
            if (d_userData[0] != 0) begin
                f_userData[0] = d_userData[0];
            end
        end
    end
    jtaglet #(
          .IR_LEN    (5)
        , .ID_PARTVER(4'h5)
        , .ID_PARTNUM(16'h3817)
        , .ID_MANF   (11'h482)
    ) i_jtaglet (
        .*
        , .trst        (w_trst)
        , .userData_in (f_userData[0])
        , .userData_out(d_userData[0])
        , .userOp      ()
        , .userOp_ready()
    );

    //`ifdef COCOTB_SIM
`ifdef COCOTB_ICARUS
    initial begin
        $dumpfile("dut.vcd");
        $dumpvars(0, dut);
        /* verilator lint_off STMTDLY */
        #1;
        /* verilator lint_on STMTDLY */
    end
`endif

endmodule

