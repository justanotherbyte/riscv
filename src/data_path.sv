module data_path(
  input logic clk
);
  logic [31:0] pc_next, pc, pc_plus_4, pc_target, instr, rs1_value, alu_result, read_data, write_data, result, src_b;
  logic [31:0] imm_ext;

  logic reg_file_WE = 1;
  logic data_mem_WE = 0;
  logic [1:0] imm_src = 0;
  logic result_src = 1;
  logic alu_src = 1;
  logic [2:0] alu_ctrl = 3'b000;
  logic pc_src = 0;

  assign pc_next = pc_src ? pc_target : pc_plus_4;

  program_counter prog_counter ( .pc_next(pc_next), .pc(pc), .clk(clk) );
  ins_mem ins_mem ( .A(pc), .RD(instr) );

  assign result = result_src ? read_data : alu_result;

  reg_file reg_file (
    .A1(instr[19:15]),
    .A2(instr[24:20]),
    .A3(instr[11:7]),
    .clk(clk),
    .WE3(reg_file_WE),
    .RD1(rs1_value),
    .RD2(write_data),
    .WD3(result)
  );

  extend ext (
    .imm(instr[31:7]),
    .imm_src(imm_src),
    .imm_ext(imm_ext)
  );

  assign src_b = alu_src ? imm_ext : write_data;

  alu alu (
    .src_a(rs1_value),
    .src_b(src_b),
    .ctrl(alu_ctrl),
    .result(alu_result)
  );

  alu pc_alu (
    .src_a(pc),
    .src_b(4),
    .result(pc_plus_4)
  );

  alu pc_branch_alu (
    .src_a(pc),
    .src_b(imm_ext),
    .ctrl(3'b000),
    .result(pc_target)
  );

  data_mem data_mem (
    .clk(clk),
    .WE(data_mem_WE),
    .A(alu_result),
    .WD(write_data),
    .RD(read_data)
  );

endmodule
