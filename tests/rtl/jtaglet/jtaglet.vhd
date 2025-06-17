-- This VHDL was converted from Verilog using the
-- Icarus Verilog VHDL Code Generator 13.0 (devel) (8cd7bb3)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module ff_sync (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/ff_sync.v:15)
--   WIDTH = 1
entity ff_sync is
  port (
    clk : in std_logic;
    in_async : in std_logic;
    out_sig : out std_logic;
    rst_p : in std_logic
  );
end entity;

-- Generated from Verilog module ff_sync (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/ff_sync.v:15)
--   WIDTH = 1
architecture from_verilog of ff_sync is
  signal out_sig_Reg : std_logic;
  signal sync_reg : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/ff_sync.v:24
begin
  out_sig <= out_sig_Reg;

  -- Generated from always process in ff_sync (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/ff_sync.v:25)
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

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtaglet (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:22)
--   BYPASS_OP = 31
--   IDCODE_OP = 30
--   ID_MANF = 1154
--   ID_PARTNUM = 14359
--   ID_PARTVER = 5
--   IR_LEN = 5
--   USERDATA_LEN = 32
--   USERDATA_OP = 8
--   USEROP_LEN = 8
--   USEROP_OP = 9
entity jtaglet is
  port (
    tck : in std_logic;
    tdi : in std_logic;
    tdo : out std_logic;
    tms : in std_logic;
    trst : in std_logic;
    userData_in : in unsigned(31 downto 0);
    userData_out : out unsigned(31 downto 0);
    userOp : out unsigned(7 downto 0);
    userOp_ready : out std_logic
  );
end entity;

-- Generated from Verilog module jtaglet (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:22)
--   BYPASS_OP = 31
--   IDCODE_OP = 30
--   ID_MANF = 1154
--   ID_PARTNUM = 14359
--   ID_PARTVER = 5
--   IR_LEN = 5
--   USERDATA_LEN = 32
--   USERDATA_OP = 8
--   USEROP_LEN = 8
--   USEROP_OP = 9
architecture from_verilog of jtaglet is
  signal tdo_Reg : std_logic;
  signal bypass_tdo : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:130
  signal idcode : unsigned(31 downto 0);  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:47
  signal idcode_tdo : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:109
  signal ir_reg : unsigned(4 downto 0);  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:64
  signal ir_tdo : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:151
  signal state_capturedr : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal state_captureir : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal state_shiftdr : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal state_shiftir : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal state_tlr : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal state_updatedr : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal state_updateir : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:49
  signal tdo_pre : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:167
  signal userData_tdo : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:67
  signal userOp_tdo : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:88

  component jtag_reg is
    port (
      dr_dataIn : in std_logic;
      dr_dataOut : out std_logic;
      dr_dataOutReady : out std_logic;
      ir_reg : in unsigned(4 downto 0);
      state_capturedr : in std_logic;
      state_shiftdr : in std_logic;
      state_tlr : in std_logic;
      state_updatedr : in std_logic;
      tck : in std_logic;
      tdi : in std_logic;
      tdo : out std_logic;
      trst : in std_logic
    );
  end component;

  component jtag_reg1 is
    port (
      dr_dataIn : in unsigned(31 downto 0);
      dr_dataOut : out unsigned(31 downto 0);
      dr_dataOutReady : out std_logic;
      ir_reg : in unsigned(4 downto 0);
      state_capturedr : in std_logic;
      state_shiftdr : in std_logic;
      state_tlr : in std_logic;
      state_updatedr : in std_logic;
      tck : in std_logic;
      tdi : in std_logic;
      tdo : out std_logic;
      trst : in std_logic
    );
  end component;

  component jtag_state_machine is
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
  end component;

  component jtag_reg2 is
    port (
      dr_dataIn : in unsigned(31 downto 0);
      dr_dataOut : out unsigned(31 downto 0);
      dr_dataOutReady : out std_logic;
      ir_reg : in unsigned(4 downto 0);
      state_capturedr : in std_logic;
      state_shiftdr : in std_logic;
      state_tlr : in std_logic;
      state_updatedr : in std_logic;
      tck : in std_logic;
      tdi : in std_logic;
      tdo : out std_logic;
      trst : in std_logic
    );
  end component;
  signal dr_dataOut_Readable : unsigned(31 downto 0);  -- Needed to connect outputs

  component jtag_reg3 is
    port (
      dr_dataIn : in unsigned(7 downto 0);
      dr_dataOut : out unsigned(7 downto 0);
      dr_dataOutReady : out std_logic;
      ir_reg : in unsigned(4 downto 0);
      state_capturedr : in std_logic;
      state_shiftdr : in std_logic;
      state_tlr : in std_logic;
      state_updatedr : in std_logic;
      tck : in std_logic;
      tdi : in std_logic;
      tdo : out std_logic;
      trst : in std_logic
    );
  end component;
  signal dr_dataOutReady_Readable : std_logic;  -- Needed to connect outputs
begin
  tdo <= tdo_Reg;
  ir_tdo <= ir_reg(0);

  -- Generated from instantiation at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:135
  bypass_reg: jtag_reg
    port map (
      dr_dataIn => '0',
      ir_reg => ir_reg,
      state_capturedr => state_capturedr,
      state_shiftdr => state_shiftdr,
      state_tlr => state_tlr,
      state_updatedr => '0',
      tck => tck,
      tdi => tdi,
      tdo => bypass_tdo,
      trst => trst
    );

  -- Generated from instantiation at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:114
  idcode_reg: jtag_reg1
    port map (
      dr_dataIn => idcode,
      ir_reg => ir_reg,
      state_capturedr => state_capturedr,
      state_shiftdr => state_shiftdr,
      state_tlr => state_tlr,
      state_updatedr => '0',
      tck => tck,
      tdi => tdi,
      tdo => idcode_tdo,
      trst => trst
    );

  -- Generated from instantiation at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:51
  jsm: jtag_state_machine
    port map (
      state_capturedr => state_capturedr,
      state_captureir => state_captureir,
      state_shiftdr => state_shiftdr,
      state_shiftir => state_shiftir,
      state_tlr => state_tlr,
      state_updatedr => state_updatedr,
      state_updateir => state_updateir,
      tck => tck,
      tms => tms,
      trst => trst
    );
  userData_out <= dr_dataOut_Readable;

  -- Generated from instantiation at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:72
  userData_reg: jtag_reg2
    port map (
      dr_dataIn => userData_in,
      dr_dataOut => dr_dataOut_Readable,
      ir_reg => ir_reg,
      state_capturedr => state_capturedr,
      state_shiftdr => state_shiftdr,
      state_tlr => state_tlr,
      state_updatedr => state_updatedr,
      tck => tck,
      tdi => tdi,
      tdo => userData_tdo,
      trst => trst
    );
  userOp_ready <= dr_dataOutReady_Readable;

  -- Generated from instantiation at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:93
  userOp_reg: jtag_reg3
    port map (
      dr_dataIn => X"00",
      dr_dataOut => userOp,
      dr_dataOutReady => dr_dataOutReady_Readable,
      ir_reg => ir_reg,
      state_capturedr => state_capturedr,
      state_shiftdr => state_shiftdr,
      state_tlr => state_tlr,
      state_updatedr => state_updatedr,
      tck => tck,
      tdi => tdi,
      tdo => userOp_tdo,
      trst => trst
    );
  idcode <= X"53817905";

  -- Generated from always process in jtaglet (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:153)
  process (tck, trst) is
  begin
    if (not trst) = '1' then
      ir_reg <= "11110";
    elsif rising_edge(tck) then
      if state_tlr = '1' then
        ir_reg <= "11110";
      else
        if state_captureir = '1' then
          ir_reg <= "00001";
        else
          if state_shiftir = '1' then
            ir_reg <= tdi & ir_reg(1 + 3 downto 1);
          end if;
        end if;
      end if;
    end if;
  end process;

  -- Generated from always process in jtaglet (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:168)
  process (state_shiftdr, ir_reg, idcode_tdo, bypass_tdo, userData_tdo, userOp_tdo, state_shiftir, ir_tdo) is
  begin
    tdo_pre <= '0';
    if state_shiftdr = '1' then
      case ir_reg is
        when "11110" =>
          tdo_pre <= idcode_tdo;
        when "11111" =>
          tdo_pre <= bypass_tdo;
        when "01000" =>
          tdo_pre <= userData_tdo;
        when "01001" =>
          tdo_pre <= userOp_tdo;
        when others =>
          tdo_pre <= bypass_tdo;
      end case;
    else
      if state_shiftir = '1' then
        tdo_pre <= ir_tdo;
      end if;
    end if;
  end process;

  -- Generated from always process in jtaglet (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtaglet.v:184)
  process (tck) is
  begin
    if falling_edge(tck) then
      tdo_Reg <= tdo_pre;
    end if;
  end process;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 1
--   IR_LEN = 5
--   IR_OPCODE = 31
entity jtag_reg is
  port (
    dr_dataIn : in std_logic;
    dr_dataOut : out std_logic;
    dr_dataOutReady : out std_logic;
    ir_reg : in unsigned(4 downto 0);
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

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 1
--   IR_LEN = 5
--   IR_OPCODE = 31
architecture from_verilog of jtag_reg is
  signal dr_dataOut_Reg : std_logic;
  signal dr_dataOutReady_Reg : std_logic;
  signal dr_reg : std_logic;  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:41
begin
  dr_dataOut <= dr_dataOut_Reg;
  dr_dataOutReady <= dr_dataOutReady_Reg;
  tdo <= dr_reg;

  -- Generated from always process in jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:45)
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
      if ir_reg = "11111" then
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

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 32
--   IR_LEN = 5
--   IR_OPCODE = 30
entity jtag_reg1 is
  port (
    dr_dataIn : in unsigned(31 downto 0);
    dr_dataOut : out unsigned(31 downto 0);
    dr_dataOutReady : out std_logic;
    ir_reg : in unsigned(4 downto 0);
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

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 32
--   IR_LEN = 5
--   IR_OPCODE = 30
architecture from_verilog of jtag_reg1 is
  signal dr_dataOut_Reg : unsigned(31 downto 0);
  signal dr_dataOutReady_Reg : std_logic;
  signal dr_reg : unsigned(31 downto 0);  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:41
begin
  dr_dataOut <= dr_dataOut_Reg;
  dr_dataOutReady <= dr_dataOutReady_Reg;
  tdo <= dr_reg(0);

  -- Generated from always process in jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:45)
  process (tck, trst) is
  begin
    if (not trst) = '1' then
      dr_reg <= X"00000000";
      dr_dataOut_Reg <= X"00000000";
      dr_dataOutReady_Reg <= '0';
    elsif rising_edge(tck) then
      dr_dataOutReady_Reg <= '0';
      if state_tlr = '1' then
        dr_reg <= dr_dataIn;
      end if;
      if ir_reg = "11110" then
        if state_capturedr = '1' then
          dr_reg <= dr_dataIn;
        else
          if state_shiftdr = '1' then
            dr_reg <= tdi & dr_reg(1 + 30 downto 1);
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

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_state_machine (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:22)
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

-- Generated from Verilog module jtag_state_machine (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:22)
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
  signal tmp_ivl_0 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:37
  signal tmp_ivl_12 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:41
  signal tmp_ivl_16 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:48
  signal tmp_ivl_20 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:45
  signal tmp_ivl_24 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:52
  signal tmp_ivl_4 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:40
  signal tmp_ivl_8 : unsigned(3 downto 0);  -- Temporary created at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:47
  signal state : unsigned(3 downto 0);  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:54
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

  -- Generated from always process in jtag_state_machine (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_state_machine.v:56)
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

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 32
--   IR_LEN = 5
--   IR_OPCODE = 8
entity jtag_reg2 is
  port (
    dr_dataIn : in unsigned(31 downto 0);
    dr_dataOut : out unsigned(31 downto 0);
    dr_dataOutReady : out std_logic;
    ir_reg : in unsigned(4 downto 0);
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

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 32
--   IR_LEN = 5
--   IR_OPCODE = 8
architecture from_verilog of jtag_reg2 is
  signal dr_dataOut_Reg : unsigned(31 downto 0);
  signal dr_dataOutReady_Reg : std_logic;
  signal dr_reg : unsigned(31 downto 0);  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:41
begin
  dr_dataOut <= dr_dataOut_Reg;
  dr_dataOutReady <= dr_dataOutReady_Reg;
  tdo <= dr_reg(0);

  -- Generated from always process in jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:45)
  process (tck, trst) is
  begin
    if (not trst) = '1' then
      dr_reg <= X"00000000";
      dr_dataOut_Reg <= X"00000000";
      dr_dataOutReady_Reg <= '0';
    elsif rising_edge(tck) then
      dr_dataOutReady_Reg <= '0';
      if state_tlr = '1' then
        dr_reg <= dr_dataIn;
      end if;
      if ir_reg = "01000" then
        if state_capturedr = '1' then
          dr_reg <= dr_dataIn;
        else
          if state_shiftdr = '1' then
            dr_reg <= tdi & dr_reg(1 + 30 downto 1);
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

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 8
--   IR_LEN = 5
--   IR_OPCODE = 9
entity jtag_reg3 is
  port (
    dr_dataIn : in unsigned(7 downto 0);
    dr_dataOut : out unsigned(7 downto 0);
    dr_dataOutReady : out std_logic;
    ir_reg : in unsigned(4 downto 0);
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

-- Generated from Verilog module jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:22)
--   DR_LEN = 8
--   IR_LEN = 5
--   IR_OPCODE = 9
architecture from_verilog of jtag_reg3 is
  signal dr_dataOut_Reg : unsigned(7 downto 0);
  signal dr_dataOutReady_Reg : std_logic;
  signal dr_reg : unsigned(7 downto 0);  -- Declared at /mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:41
begin
  dr_dataOut <= dr_dataOut_Reg;
  dr_dataOutReady <= dr_dataOutReady_Reg;
  tdo <= dr_reg(0);

  -- Generated from always process in jtag_reg (/mnt/sda/projects/cocotbext-jtag/tests/rtl/jtaglet/jtag_reg.v:45)
  process (tck, trst) is
  begin
    if (not trst) = '1' then
      dr_reg <= X"00";
      dr_dataOut_Reg <= X"00";
      dr_dataOutReady_Reg <= '0';
    elsif rising_edge(tck) then
      dr_dataOutReady_Reg <= '0';
      if state_tlr = '1' then
        dr_reg <= dr_dataIn;
      end if;
      if ir_reg = "01001" then
        if state_capturedr = '1' then
          dr_reg <= dr_dataIn;
        else
          if state_shiftdr = '1' then
            dr_reg <= tdi & dr_reg(1 + 6 downto 1);
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
