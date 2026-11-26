module extend (
  input logic [31:7] imm,
  input logic imm_src,
  output logic [31:0] imm_ext
);

  logic [11:0] chosen_imm;
  assign chosen_imm = imm_src ? { imm[31:25], imm[11:7] } : imm[31:20];

  assign imm_ext = { {20{chosen_imm[11]}}, chosen_imm };

endmodule
