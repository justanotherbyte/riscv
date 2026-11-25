module data_mem(
  input logic clk, WE,
  input logic [31:0] A,
  input logic [31:0] WD,
  output logic [31:0] RD
);

  logic [31:0] mem [0:63];

  assign RD = mem[A[7:2]];

  always_ff @( posedge clk ) begin
    if (WE) begin
      mem[A[7:2]] <= WD;
    end
  end

endmodule
