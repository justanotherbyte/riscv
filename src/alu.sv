module alu (
  input logic [31:0] src_a,
  input logic [31:0] src_b,
  input logic [2:0] ctrl,
  output logic [31:0] result,
  output logic zero
);

  logic [31:0] diff;
  assign diff = src_a - src_b;

  always_comb begin : mux_alu
    case (ctrl)
      3'b000: result = src_a + src_b;
      3'b001: result = src_a - src_b;
      3'b010: result = src_a & src_b;
      3'b011: result = src_a | src_b;
      3'b101: result = (src_a[31] != src_b[31]) ? { 31'b0, src_a[31] } : { 31'b0, diff[31] };
      default: result = 32'b0;
    endcase
  end

  assign zero = (result == 32'b0) ? 1 : 0;

endmodule
