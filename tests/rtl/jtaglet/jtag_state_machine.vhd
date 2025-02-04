-- This VHDL was converted from Verilog using the
-- Icarus Verilog VHDL Code Generator 13.0 (devel) (8cd7bb3)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_state_machine (jtag_state_machine.v:22)
--   CAPTURE_DR = 3
--   CAPTURE_IR = 10
--   EXIT1_DR = 5
--   EXIT1_IR = 12
--   EXIT2_DR = 7
--   EXIT2_IR = 14
--   PAUSE_DR = 6
--   PAUSE_IR = 13
--   RUN_TEST_IDLE = 1
--   SELECT_DR = 2
--   SELECT_IR = 9
--   SHIFT_DR = 4
--   SHIFT_IR = 11
--   TEST_LOGIC_RESET = 0
--   UPDATE_DR = 8
--   UPDATE_IR = 15
entity jtag_state_machine is
  port (
    state_capturedr : out std_logic;
    state_captureir : out std_logic;
    state_shiftdr : out std_logic;
    state_shiftir : out std_logic;
    state_tlr : out std_logic;
    state_updatedr : out std_logic;
    state_updateir : out std_logic;
    tck : in std_logic;
    tms : in std_logic;
    trst : in std_logic
  );
end entity; 

-- Generated from Verilog module jtag_state_machine (jtag_state_machine.v:22)
--   CAPTURE_DR = 3
--   CAPTURE_IR = 10
--   EXIT1_DR = 5
--   EXIT1_IR = 12
--   EXIT2_DR = 7
--   EXIT2_IR = 14
--   PAUSE_DR = 6
--   PAUSE_IR = 13
--   RUN_TEST_IDLE = 1
--   SELECT_DR = 2
--   SELECT_IR = 9
--   SHIFT_DR = 4
--   SHIFT_IR = 11
--   TEST_LOGIC_RESET = 0
--   UPDATE_DR = 8
--   UPDATE_IR = 15
architecture from_verilog of jtag_state_machine is
  signal tmp_ivl_0 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:37
  signal tmp_ivl_12 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:41
  signal tmp_ivl_16 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:48
  signal tmp_ivl_20 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:45
  signal tmp_ivl_24 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:52
  signal tmp_ivl_4 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:40
  signal tmp_ivl_8 : unsigned(3 downto 0);  -- Temporary created at jtag_state_machine.v:47
  signal state : unsigned(3 downto 0);  -- Declared at jtag_state_machine.v:54
begin
  state_tlr <= '1' when state = tmp_ivl_0 else '0';
  state_capturedr <= '1' when state = tmp_ivl_4 else '0';
  state_captureir <= '1' when state = tmp_ivl_8 else '0';
  state_shiftdr <= '1' when state = tmp_ivl_12 else '0';
  state_shiftir <= '1' when state = tmp_ivl_16 else '0';
  state_updatedr <= '1' when state = tmp_ivl_20 else '0';
  state_updateir <= '1' when state = tmp_ivl_24 else '0';
  tmp_ivl_0 <= X"0";
  tmp_ivl_12 <= X"4";
  tmp_ivl_16 <= X"b";
  tmp_ivl_20 <= X"8";
  tmp_ivl_24 <= X"f";
  tmp_ivl_4 <= X"3";
  tmp_ivl_8 <= X"a";
  
  -- Generated from always process in jtag_state_machine (jtag_state_machine.v:56)
  process (tck, trst) is
  begin
    if (not trst) = '1' then
      state <= X"0";
    elsif rising_edge(tck) then
      case state is
        when X"0" =>
          if tms = '1' then
            state <= X"0";
          else
            state <= X"1";
          end if;
        when X"1" =>
          if tms = '1' then
            state <= X"2";
          else
            state <= X"1";
          end if;
        when X"2" =>
          if tms = '1' then
            state <= X"9";
          else
            state <= X"3";
          end if;
        when X"3" =>
          if tms = '1' then
            state <= X"5";
          else
            state <= X"4";
          end if;
        when X"4" =>
          if tms = '1' then
            state <= X"5";
          else
            state <= X"4";
          end if;
        when X"5" =>
          if tms = '1' then
            state <= X"8";
          else
            state <= X"6";
          end if;
        when X"6" =>
          if tms = '1' then
            state <= X"7";
          else
            state <= X"6";
          end if;
        when X"7" =>
          if tms = '1' then
            state <= X"8";
          else
            state <= X"4";
          end if;
        when X"8" =>
          if tms = '1' then
            state <= X"2";
          else
            state <= X"1";
          end if;
        when X"9" =>
          if tms = '1' then
            state <= X"0";
          else
            state <= X"a";
          end if;
        when X"a" =>
          if tms = '1' then
            state <= X"c";
          else
            state <= X"b";
          end if;
        when X"b" =>
          if tms = '1' then
            state <= X"c";
          else
            state <= X"b";
          end if;
        when X"c" =>
          if tms = '1' then
            state <= X"f";
          else
            state <= X"d";
          end if;
        when X"d" =>
          if tms = '1' then
            state <= X"e";
          else
            state <= X"d";
          end if;
        when X"e" =>
          if tms = '1' then
            state <= X"f";
          else
            state <= X"b";
          end if;
        when X"f" =>
          if tms = '1' then
            state <= X"2";
          else
            state <= X"1";
          end if;
        when others =>
          null;
      end case;
    end if;
  end process;
end architecture;

