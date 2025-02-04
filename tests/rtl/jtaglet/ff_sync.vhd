-- This VHDL was converted from Verilog using the
-- Icarus Verilog VHDL Code Generator 13.0 (devel) (8cd7bb3)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module ff_sync (ff_sync.v:15)
--   WIDTH = 1
entity ff_sync is
  port (
    clk : in std_logic;
    in_async : in std_logic;
    out_sig : out std_logic;
    rst_p : in std_logic
  );
end entity; 

-- Generated from Verilog module ff_sync (ff_sync.v:15)
--   WIDTH = 1
architecture from_verilog of ff_sync is
  signal out_sig_Reg : std_logic;
  signal sync_reg : std_logic;  -- Declared at ff_sync.v:24
begin
  out_sig <= out_sig_Reg;
  
  -- Generated from always process in ff_sync (ff_sync.v:25)
  process (clk, rst_p) is
    variable Verilog_Assign_Tmp_0 : unsigned(1 downto 0);
  begin
    if rst_p = '1' then
      sync_reg <= '0';
      out_sig_Reg <= '0';
    elsif rising_edge(clk) then
      Verilog_Assign_Tmp_0 := sync_reg & in_async;
      sync_reg <= Verilog_Assign_Tmp_0(0);
      out_sig_Reg <= Verilog_Assign_Tmp_0(1);
    end if;
  end process;
end architecture;

