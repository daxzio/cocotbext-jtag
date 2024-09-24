module dut (
      input      clkin
    , input      rst
    , input      tck
    , input      tms
    , input      tdi
    , output reg tdo
    , output     uart_tx
    , input      uart_rx
);

    localparam integer G_NUM_JTAG = 1;
    logic [G_NUM_JTAG:0] w_td;

    //     logic                  w_trst;


    assign w_td[0] = tdi;

    top_soc i_top_soc (
        .*
        //         , .trst_n        (w_trst)
        , .tdi(w_td[0])
        , .tdo(w_td[1])
    );

    assign tdo = w_td[G_NUM_JTAG];


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

