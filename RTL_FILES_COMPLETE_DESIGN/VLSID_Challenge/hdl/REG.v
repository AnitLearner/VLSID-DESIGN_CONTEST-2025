`timescale 1ns / 1ps

module REG #(parameter DATAW=10)
            (input clk,
             input reset,
             input [DATAW-1:0]in,
             output reg [DATAW-1:0]out);

always @(posedge clk)
begin
    if (reset)
    begin
        out <= 0;
    end
    else
    begin
        out <= in;
    end
end

endmodule

