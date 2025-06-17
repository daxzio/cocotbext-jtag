-- This VHDL was converted from Verilog using the
-- Icarus Verilog VHDL Code Generator 13.0 (devel) (8cd7bb3)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_reg (jtag_reg.v:22)
--   DR_LEN = 1
--   IR_LEN = 4
--   IR_OPCODE = 0
entity jtag_reg is
  port (
    dr_dataIn : in std_logic;
    dr_dataOut : out std_logic;
    dr_dataOutReady : out std_logic;
    ir_reg : in unsigned(3 downto 0);
    state_capturedr : in std_logic;
    state_shiftdr : in std_logic;
    state_tlr : in std_logic;
    state_updatedr : in std_logic;
    tck : in std_logic;
    tdi : in std_logic;
    tdo : out std_logic;
    trst : in std_logic
  );
end entity;

-- Generated from Verilog module jtag_reg (jtag_reg.v:22)
--   DR_LEN = 1
--   IR_LEN = 4
--   IR_OPCODE = 0
architecture from_verilog of jtag_reg is
  signal dr_dataOut_Reg : std_logic;
  signal dr_dataOutReady_Reg : std_logic;
  signal dr_reg : std_logic;  -- Declared at jtag_reg.v:41
begin
  dr_dataOut <= dr_dataOut_Reg;
  dr_dataOutReady <= dr_dataOutReady_Reg;
  tdo <= dr_reg;

  -- Generated from always process in jtag_reg (jtag_reg.v:45)
  process (tck, trst) is
  begin
    if (not trst) = '1' then
      dr_reg <= '0';
      dr_dataOut_Reg <= '0';
      dr_dataOutReady_Reg <= '0';
    elsif rising_edge(tck) then
      dr_dataOutReady_Reg <= '0';
      if state_tlr = '1' then
        dr_reg <= dr_dataIn;
      end if;
      if ir_reg = X"0" then
        if state_capturedr = '1' then
          dr_reg <= dr_dataIn;
        else
          if state_shiftdr = '1' then
            dr_reg <= tdi;
          else
            if state_updatedr = '1' then
              dr_dataOut_Reg <= dr_reg;
              dr_dataOutReady_Reg <= '1';
            end if;
          end if;
        end if;
      end if;
    end if;
  end process;
end architecture;
