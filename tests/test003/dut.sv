module dut (
      input      a
    , input      b
    , input      c
    , output reg d
    , input      trst
);

    localparam integer G_NUM_JTAG = 1;
    logic [G_NUM_JTAG-1:0] w_td;

    logic                  w_trst;
    logic                  w_tck;

    logic [          31:0] d_userData[G_NUM_JTAG-1:0];
    logic [          31:0] f_userData[G_NUM_JTAG-1:0];

    assign w_trst = trst;
    assign w_tck = a;

    always @(posedge w_tck or negedge w_trst) begin
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
          .tck        (a)
        , .tms        (b)
        , .tdi        (c)
        , .tdo        (d)
        , .trst        (w_trst)
        , .userData_in (f_userData[0])
        , .userData_out(d_userData[0])
        , .userOp      ()
        , .userOp_ready()
    );


endmodule
