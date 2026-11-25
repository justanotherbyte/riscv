module alu (
  input logic [31:0] src_a,
  input logic [31:0] src_b,
  input logic [2:0] ctrl,
  output logic [31:0] result
);


  always_comb begin : mux_alu
    case (ctrl)
      3'b000: result = src_a + src_b;
      default: result = src_a - src_b;
    endcase
  end


endmodule
