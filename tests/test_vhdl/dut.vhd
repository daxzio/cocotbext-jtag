library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity dut is
  port (
    tck  : in std_logic;
    tms  : in std_logic;
    tdi  : in std_logic;
    tdo  : out std_logic;
    trst : in std_logic
  );
end entity;

architecture tb of dut is
    signal d_userData : unsigned(31 downto 0);
    signal f_userData : unsigned(31 downto 0);
    signal wtrst : std_logic;

    component jtaglet is
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
    end component;

begin


    wtrst <= trst;

    i_jtaglet: jtaglet
      port map (
        tck => tck,
        tdi => tdi,
        tdo => tdo,
        tms => tms,
        trst => wtrst,
        userData_in => f_userData,
        userData_out => d_userData,
        userOp => open,
        userOp_ready => open
      );

      process (tck, trst) is
      begin
          if trst = '0' then
              f_userData <= X"e6712945";
          elsif rising_edge(tck) then
              if d_userData /= x"00000000" then
                  f_userData <= d_userData;
              end if;
          end if;
      end process;

end;
