module extend (
  input logic [31:7] imm,
  input logic [1:0] imm_src,
  output logic [31:0] imm_ext
);

  always_comb begin : mux_imm_ext 
    case (imm_src)
      2'b00: imm_ext = { {20{imm[31]}}, imm[31:20] };
      2'b01: imm_ext = { {20{imm[31]}}, imm[31:25], imm[11:7] };
      2'b10: imm_ext = { {20{imm[31]}}, imm[7], imm[30:25], imm[11:8], 1'b0 };
      default: imm_ext = 'x;
    endcase
  end

endmodule
