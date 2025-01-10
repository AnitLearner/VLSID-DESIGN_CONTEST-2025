`timescale 1ns / 1ps


module LFSR53(input clk,
            input set,
            output out);
            
wire r1,r2,r3,r4,r5;
reg reset = 0;

reg1b reg1(.clk(clk),
           .in(r1),
           .out(r2),
           .reset(set),
           .set(reset));   
           
reg1b reg2(.clk(clk),
           .in(r2),
           .out(r3),
           .reset(reset),
           .set(set));
           
reg1b reg3(.clk(clk),
           .in(r3),
           .out(r4),
           .reset(reset),
           .set(set));
           
reg1b reg4(.clk(clk),
           .in(r4),
           .out(r5),
           .reset(set),
           .set(reset));
           
reg1b reg5(.clk(clk),
           .in(r5),
           .out(out),
           .reset(set),
           .set(reset));
           
assign r1 = (r4) ^ (out);
          
endmodule