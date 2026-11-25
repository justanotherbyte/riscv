module reg_file(
  input logic [4:0] A1, A2, A3,
  input logic [31:0] WD3,
  input logic clk, WE3,
  output logic [31:0] RD1, RD2
);

  logic [31:0] mem [1:31];

  assign RD1 = A1 != 0 ? mem[A1] : '0;
  assign RD2 = A2 != 0 ? mem[A2] : '0;

  always_ff @( posedge clk ) begin : write_A3
    if (WE3 && A3 != 0) begin
      mem[A3] <= WD3;
    end
  end

endmodule