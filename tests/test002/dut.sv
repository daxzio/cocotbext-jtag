module dut (
      input tck
    , input tms
    , input tdi
    , output reg tdo
    , input trst
);

    localparam integer G_NUM_JTAG = 3;
    logic [G_NUM_JTAG:0] w_td;
    assign w_td[0] = tdi;
    assign tdo = w_td[G_NUM_JTAG];

    logic [31:0] d_userData [G_NUM_JTAG-1:0];
    logic [31:0] f_userData [G_NUM_JTAG-1:0];

    always @(posedge tck or negedge trst) begin
        if (!trst) begin
            f_userData[0] = 32'he6712945; 
            f_userData[1] = 32'h46834257; 
            f_userData[2] = 32'h98754ae7; 
        end else begin
            if (d_userData[0] != 0) begin
                f_userData[0] = d_userData[0];
            end 
            if (d_userData[1] != 0) begin
                f_userData[1] = d_userData[1];
            end 
            if (d_userData[2] != 0) begin
                f_userData[2] = d_userData[2];
            end 
        end
    end
    

    jtaglet # (
          .IR_LEN     (4)
        , .ID_PARTVER (4'h5)
        , .ID_PARTNUM (16'h3817)
        , .ID_MANF    (11'h482)
    )
    i_jtaglet_0 (
        .*
        , .tdi         (w_td[0])
        , .tdo         (w_td[1])
        , .userData_in (f_userData[0])
        , .userData_out (d_userData[0])
        , .userOp ( )
        , .userOp_ready ( )
    );
    
    jtaglet # (
          .IR_LEN     (5)
        , .ID_PARTVER (4'hc)
        , .ID_PARTNUM (16'h8215)
        , .ID_MANF    (11'h619)
    )
    i_jtaglet_1 (
        .*
        , .tdi         (w_td[1])
        , .tdo         (w_td[2])
        , .userData_in (f_userData[1])
        , .userData_out (d_userData[1])
        , .userOp ( )
        , .userOp_ready ( )
    );
    
    jtaglet # (
          .IR_LEN     (4)
        , .ID_PARTVER (4'ha)
        , .ID_PARTNUM (16'h9243)
        , .ID_MANF    (11'h267)
    )
    i_jtaglet_2 (
        .*
        , .tdi         (w_td[2])
        , .tdo         (w_td[3])
        , .userData_in (f_userData[2])
        , .userData_out (d_userData[2])
        , .userOp ( )
        , .userOp_ready ( )
    );
   

endmodule

