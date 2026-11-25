module riscv(
  input logic clk
);
  logic [31:0] pc_next, pc, instr, rs1_value, alu_result, read_data;
  logic [31:0] imm_ext;

  logic reg_file_WE = 1;
  logic data_mem_WE = 0;

  program_counter prog_counter ( .pc_next(pc_next), .pc(pc), .clk(clk) );
  ins_mem ins_mem ( .A(pc), .RD(instr) );
  reg_file reg_file (
    .A1(instr[19:15]),
    .A3(instr[11:7]),
    .clk(clk),
    .WE3(reg_file_WE),
    .RD1(rs1_value),
    .WD3(read_data)
  );

  extend ext (
    .imm(instr[31:20]),
    .imm_ext(imm_ext)
  );

  alu alu (
    .src_a(rs1_value),
    .src_b(imm_ext),
    .ctrl(0),
    .result(alu_result)
  );

  alu pc_alu (
    .src_a(pc),
    .src_b(4),
    .result(pc_next)
  );

  data_mem data_mem (
    .clk(clk),
    .WE(data_mem_WE),
    .A(alu_result),
    .WD(),
    .RD(read_data)
  );

endmodule
