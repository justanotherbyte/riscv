module ins_mem (
  input logic [31:0] A,
  output logic [31:0] RD
);

  logic [31:0] mem [0:63];
  assign RD = mem[A[7:2]];
endmodule