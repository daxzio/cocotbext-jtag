/*****************************************************************************\
|                      Copyright (C) 2021-2022 Luke Wren                      |
|                     SPDX-License-Identifier: Apache-2.0                     |
\*****************************************************************************/

localparam RV_RS1_LSB = 15;
localparam RV_RS1_BITS = 5;
localparam RV_RS2_LSB = 20;
localparam RV_RS2_BITS = 5;
localparam RV_RD_LSB = 7;
localparam RV_RD_BITS = 5;

// Note: these are preprocessor macros, rather than the usual localparams,
// because it's quite difficult to get a definitive citation from 1364-2005
// for whether Z values are propagated through a localparam to a casez.
// Multiple tools complain about it, so just this once I'll use macros.

`ifndef HAZARD3_RVOPC_MACROS
`define HAZARD3_RVOPC_MACROS

// Base ISA (some of these are Z now)
`define RVOPC_BEQ         32'b?????????????????000?????1100011
`define RVOPC_BNE         32'b?????????????????001?????1100011
`define RVOPC_BLT         32'b?????????????????100?????1100011
`define RVOPC_BGE         32'b?????????????????101?????1100011
`define RVOPC_BLTU        32'b?????????????????110?????1100011
`define RVOPC_BGEU        32'b?????????????????111?????1100011
`define RVOPC_JALR        32'b?????????????????000?????1100111
`define RVOPC_JAL         32'b?????????????????????????1101111
`define RVOPC_LUI         32'b?????????????????????????0110111
`define RVOPC_AUIPC       32'b?????????????????????????0010111
`define RVOPC_ADDI        32'b?????????????????000?????0010011
`define RVOPC_SLLI        32'b0000000??????????001?????0010011
`define RVOPC_SLTI        32'b?????????????????010?????0010011
`define RVOPC_SLTIU       32'b?????????????????011?????0010011
`define RVOPC_XORI        32'b?????????????????100?????0010011
`define RVOPC_SRLI        32'b0000000??????????101?????0010011
`define RVOPC_SRAI        32'b0100000??????????101?????0010011
`define RVOPC_ORI         32'b?????????????????110?????0010011
`define RVOPC_ANDI        32'b?????????????????111?????0010011
`define RVOPC_ADD         32'b0000000??????????000?????0110011
`define RVOPC_SUB         32'b0100000??????????000?????0110011
`define RVOPC_SLL         32'b0000000??????????001?????0110011
`define RVOPC_SLT         32'b0000000??????????010?????0110011
`define RVOPC_SLTU        32'b0000000??????????011?????0110011
`define RVOPC_XOR         32'b0000000??????????100?????0110011
`define RVOPC_SRL         32'b0000000??????????101?????0110011
`define RVOPC_SRA         32'b0100000??????????101?????0110011
`define RVOPC_OR          32'b0000000??????????110?????0110011
`define RVOPC_AND         32'b0000000??????????111?????0110011
`define RVOPC_LB          32'b?????????????????000?????0000011
`define RVOPC_LH          32'b?????????????????001?????0000011
`define RVOPC_LW          32'b?????????????????010?????0000011
`define RVOPC_LBU         32'b?????????????????100?????0000011
`define RVOPC_LHU         32'b?????????????????101?????0000011
`define RVOPC_SB          32'b?????????????????000?????0100011
`define RVOPC_SH          32'b?????????????????001?????0100011
`define RVOPC_SW          32'b?????????????????010?????0100011
`define RVOPC_FENCE       32'b????????????00000000000000001111
`define RVOPC_FENCE_I     32'b00000000000000000001000000001111
`define RVOPC_ECALL       32'b00000000000000000000000001110011
`define RVOPC_EBREAK      32'b00000000000100000000000001110011
`define RVOPC_CSRRW       32'b?????????????????001?????1110011
`define RVOPC_CSRRS       32'b?????????????????010?????1110011
`define RVOPC_CSRRC       32'b?????????????????011?????1110011
`define RVOPC_CSRRWI      32'b?????????????????101?????1110011
`define RVOPC_CSRRSI      32'b?????????????????110?????1110011
`define RVOPC_CSRRCI      32'b?????????????????111?????1110011
`define RVOPC_MRET        32'b00110000001000000000000001110011
`define RVOPC_SYSTEM      32'b?????????????????????????1110011
`define RVOPC_WFI         32'b00010000010100000000000001110011

// M extension
`define RVOPC_MUL         32'b0000001??????????000?????0110011
`define RVOPC_MULH        32'b0000001??????????001?????0110011
`define RVOPC_MULHSU      32'b0000001??????????010?????0110011
`define RVOPC_MULHU       32'b0000001??????????011?????0110011
`define RVOPC_DIV         32'b0000001??????????100?????0110011
`define RVOPC_DIVU        32'b0000001??????????101?????0110011
`define RVOPC_REM         32'b0000001??????????110?????0110011
`define RVOPC_REMU        32'b0000001??????????111?????0110011

// A extension
`define RVOPC_LR_W        32'b00010??00000?????010?????0101111
`define RVOPC_SC_W        32'b00011????????????010?????0101111
`define RVOPC_AMOSWAP_W   32'b00001????????????010?????0101111
`define RVOPC_AMOADD_W    32'b00000????????????010?????0101111
`define RVOPC_AMOXOR_W    32'b00100????????????010?????0101111
`define RVOPC_AMOAND_W    32'b01100????????????010?????0101111
`define RVOPC_AMOOR_W     32'b01000????????????010?????0101111
`define RVOPC_AMOMIN_W    32'b10000????????????010?????0101111
`define RVOPC_AMOMAX_W    32'b10100????????????010?????0101111
`define RVOPC_AMOMINU_W   32'b11000????????????010?????0101111
`define RVOPC_AMOMAXU_W   32'b11100????????????010?????0101111

// Zba (address generation)
`define RVOPC_SH1ADD      32'b0010000??????????010?????0110011
`define RVOPC_SH2ADD      32'b0010000??????????100?????0110011
`define RVOPC_SH3ADD      32'b0010000??????????110?????0110011

// Zbb (basic bit manipulation)
`define RVOPC_ANDN        32'b0100000??????????111?????0110011
`define RVOPC_CLZ         32'b011000000000?????001?????0010011
`define RVOPC_CPOP        32'b011000000010?????001?????0010011
`define RVOPC_CTZ         32'b011000000001?????001?????0010011
`define RVOPC_MAX         32'b0000101??????????110?????0110011
`define RVOPC_MAXU        32'b0000101??????????111?????0110011
`define RVOPC_MIN         32'b0000101??????????100?????0110011
`define RVOPC_MINU        32'b0000101??????????101?????0110011
`define RVOPC_ORC_B       32'b001010000111?????101?????0010011
`define RVOPC_ORN         32'b0100000??????????110?????0110011
`define RVOPC_REV8        32'b011010011000?????101?????0010011
`define RVOPC_ROL         32'b0110000??????????001?????0110011
`define RVOPC_ROR         32'b0110000??????????101?????0110011
`define RVOPC_RORI        32'b0110000??????????101?????0010011
`define RVOPC_SEXT_B      32'b011000000100?????001?????0010011
`define RVOPC_SEXT_H      32'b011000000101?????001?????0010011
`define RVOPC_XNOR        32'b0100000??????????100?????0110011
`define RVOPC_ZEXT_H      32'b000010000000?????100?????0110011

// Zbc (carry-less multiply)
`define RVOPC_CLMUL       32'b0000101??????????001?????0110011
`define RVOPC_CLMULH      32'b0000101??????????011?????0110011
`define RVOPC_CLMULR      32'b0000101??????????010?????0110011

// Zbs (single-bit manipulation)
`define RVOPC_BCLR        32'b0100100??????????001?????0110011
`define RVOPC_BCLRI       32'b0100100??????????001?????0010011
`define RVOPC_BEXT        32'b0100100??????????101?????0110011
`define RVOPC_BEXTI       32'b0100100??????????101?????0010011
`define RVOPC_BINV        32'b0110100??????????001?????0110011
`define RVOPC_BINVI       32'b0110100??????????001?????0010011
`define RVOPC_BSET        32'b0010100??????????001?????0110011
`define RVOPC_BSETI       32'b0010100??????????001?????0010011

// Zbkb (basic bit manipulation for crypto) (minus those in Zbb)
`define RVOPC_PACK        32'b0000100??????????100?????0110011
`define RVOPC_PACKH       32'b0000100??????????111?????0110011
`define RVOPC_BREV8       32'b011010000111?????101?????0010011
`define RVOPC_UNZIP       32'b000010001111?????101?????0010011
`define RVOPC_ZIP         32'b000010001111?????001?????0010011

// Zbkc is a subset of Zbc.

// Zbkx (crossbar permutation)
`define RVOPC_XPERM_B     32'b0010100??????????100?????0110011
`define RVOPC_XPERM_N     32'b0010100??????????010?????0110011

// Hazard3 custom instructions

// Xh3b (Hazard3 custom bitmanip): currently just a multi-bit version of bext/bexti from Zbs
`define RVOPC_H3_BEXTM    32'b000???0??????????000?????0001011 // custom-0 funct3=0
`define RVOPC_H3_BEXTMI   32'b000???0??????????100?????0001011 // custom-0 funct3=4

// C Extension
`define RVOPC_C_ADDI4SPN  16'b000???????????00 // *** illegal if imm 0
`define RVOPC_C_LW        16'b010???????????00
`define RVOPC_C_SW        16'b110???????????00

`define RVOPC_C_ADDI      16'b000???????????01
`define RVOPC_C_JAL       16'b001???????????01
`define RVOPC_C_J         16'b101???????????01
`define RVOPC_C_LI        16'b010???????????01
// addi16sp when rd=2:
`define RVOPC_C_LUI       16'b011???????????01 // *** reserved if imm 0 (for both LUI and ADDI16SP)
`define RVOPC_C_SRLI      16'b100000????????01 // On RV32 imm[5] (instr[12]) must be 0, else reserved NSE.
`define RVOPC_C_SRAI      16'b100001????????01 // On RV32 imm[5] (instr[12]) must be 0, else reserved NSE.
`define RVOPC_C_ANDI      16'b100?10????????01
`define RVOPC_C_SUB       16'b100011???00???01
`define RVOPC_C_XOR       16'b100011???01???01
`define RVOPC_C_OR        16'b100011???10???01
`define RVOPC_C_AND       16'b100011???11???01
`define RVOPC_C_BEQZ      16'b110???????????01
`define RVOPC_C_BNEZ      16'b111???????????01

`define RVOPC_C_SLLI      16'b0000??????????10 // On RV32 imm[5] (instr[12]) must be 0, else reserved NSE.
// jr if !rs2:
`define RVOPC_C_MV        16'b1000??????????10 // *** reserved if JR and !rs1 (instr[11:7])
// jalr if !rs2:
`define RVOPC_C_ADD       16'b1001??????????10 // *** EBREAK if !instr[11:2]
`define RVOPC_C_LWSP      16'b010???????????10
`define RVOPC_C_SWSP      16'b110???????????10

// Zcb simple additional compressed instructions
`define RVOPC_C_LBU       16'b100000????????00
`define RVOPC_C_LHU       16'b100001???0????00
`define RVOPC_C_LH        16'b100001???1????00
`define RVOPC_C_SB        16'b100010????????00
`define RVOPC_C_SH        16'b100011???0????00
`define RVOPC_C_ZEXT_B    16'b100111???1100001
`define RVOPC_C_SEXT_B    16'b100111???1100101
`define RVOPC_C_ZEXT_H    16'b100111???1101001
`define RVOPC_C_SEXT_H    16'b100111???1101101
`define RVOPC_C_NOT       16'b100111???1110101
`define RVOPC_C_MUL       16'b100111???10???01

// Zcmp push/pop instructions
`define RVOPC_CM_PUSH     16'b10111000??????10
`define RVOPC_CM_POP      16'b10111010??????10
`define RVOPC_CM_POPRETZ  16'b10111100??????10
`define RVOPC_CM_POPRET   16'b10111110??????10
`define RVOPC_CM_MVSA01   16'b101011???01???10
`define RVOPC_CM_MVA01S   16'b101011???11???10

// Copies provided here with 0 instead of ? so that these can be used to build 32-bit instructions in the decompressor

`define RVOPC_NOZ_BEQ     32'b00000000000000000000000001100011
`define RVOPC_NOZ_BNE     32'b00000000000000000001000001100011
`define RVOPC_NOZ_BLT     32'b00000000000000000100000001100011
`define RVOPC_NOZ_BGE     32'b00000000000000000101000001100011
`define RVOPC_NOZ_BLTU    32'b00000000000000000110000001100011
`define RVOPC_NOZ_BGEU    32'b00000000000000000111000001100011
`define RVOPC_NOZ_JALR    32'b00000000000000000000000001100111
`define RVOPC_NOZ_JAL     32'b00000000000000000000000001101111
`define RVOPC_NOZ_LUI     32'b00000000000000000000000000110111
`define RVOPC_NOZ_AUIPC   32'b00000000000000000000000000010111
`define RVOPC_NOZ_ADDI    32'b00000000000000000000000000010011
`define RVOPC_NOZ_SLLI    32'b00000000000000000001000000010011
`define RVOPC_NOZ_SLTI    32'b00000000000000000010000000010011
`define RVOPC_NOZ_SLTIU   32'b00000000000000000011000000010011
`define RVOPC_NOZ_XORI    32'b00000000000000000100000000010011
`define RVOPC_NOZ_SRLI    32'b00000000000000000101000000010011
`define RVOPC_NOZ_SRAI    32'b01000000000000000101000000010011
`define RVOPC_NOZ_ORI     32'b00000000000000000110000000010011
`define RVOPC_NOZ_ANDI    32'b00000000000000000111000000010011
`define RVOPC_NOZ_ADD     32'b00000000000000000000000000110011
`define RVOPC_NOZ_SUB     32'b01000000000000000000000000110011
`define RVOPC_NOZ_SLL     32'b00000000000000000001000000110011
`define RVOPC_NOZ_SLT     32'b00000000000000000010000000110011
`define RVOPC_NOZ_SLTU    32'b00000000000000000011000000110011
`define RVOPC_NOZ_XOR     32'b00000000000000000100000000110011
`define RVOPC_NOZ_SRL     32'b00000000000000000101000000110011
`define RVOPC_NOZ_SRA     32'b01000000000000000101000000110011
`define RVOPC_NOZ_OR      32'b00000000000000000110000000110011
`define RVOPC_NOZ_AND     32'b00000000000000000111000000110011
`define RVOPC_NOZ_LB      32'b00000000000000000000000000000011
`define RVOPC_NOZ_LH      32'b00000000000000000001000000000011
`define RVOPC_NOZ_LW      32'b00000000000000000010000000000011
`define RVOPC_NOZ_LBU     32'b00000000000000000100000000000011
`define RVOPC_NOZ_LHU     32'b00000000000000000101000000000011
`define RVOPC_NOZ_SB      32'b00000000000000000000000000100011
`define RVOPC_NOZ_SH      32'b00000000000000000001000000100011
`define RVOPC_NOZ_SW      32'b00000000000000000010000000100011
`define RVOPC_NOZ_FENCE   32'b00000000000000000000000000001111
`define RVOPC_NOZ_FENCE_I 32'b00000000000000000001000000001111
`define RVOPC_NOZ_ECALL   32'b00000000000000000000000001110011
`define RVOPC_NOZ_EBREAK  32'b00000000000100000000000001110011
`define RVOPC_NOZ_CSRRW   32'b00000000000000000001000001110011
`define RVOPC_NOZ_CSRRS   32'b00000000000000000010000001110011
`define RVOPC_NOZ_CSRRC   32'b00000000000000000011000001110011
`define RVOPC_NOZ_CSRRWI  32'b00000000000000000101000001110011
`define RVOPC_NOZ_CSRRSI  32'b00000000000000000110000001110011
`define RVOPC_NOZ_CSRRCI  32'b00000000000000000111000001110011
`define RVOPC_NOZ_SYSTEM  32'b00000000000000000000000001110011

// Non-RV32I instructions for Zcb:
`define RVOPC_NOZ_MUL     32'b00000010000000000000000000110011
`define RVOPC_NOZ_SEXT_B  32'b01100000010000000001000000010011
`define RVOPC_NOZ_SEXT_H  32'b01100000010100000001000000010011
`define RVOPC_NOZ_ZEXT_H  32'b00001000000000000100000000110011

`endif
