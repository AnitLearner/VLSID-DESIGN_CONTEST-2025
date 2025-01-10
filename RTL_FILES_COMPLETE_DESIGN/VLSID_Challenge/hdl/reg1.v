`timescale 1ns / 1ps

module reg1b (clk,in,out,reset,set);
input clk,reset,set;
input in;
output reg out;

always @(posedge clk)
begin
    if (reset)
    begin
         out <= 0;
    end
    else if (set)
    begin
         out <= 1;
    end
    else 
    begin
        out <= in;
    end
end

endmodule