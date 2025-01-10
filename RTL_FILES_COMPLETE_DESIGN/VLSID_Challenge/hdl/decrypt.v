`timescale 1ns / 1ps

module decrypt #(parameter DATAW = 16)
                (input [DATAW-1:0]data,
                input [DATAW-1:0]C,
                input dctr,
                input clk,
                input reset,
                output [DATAW-1:0]out,
                output[DATAW-1:0]data1);

wire [DATAW-1:0]w1,w4;

assign w1 = (dctr)?(data):(w4);

REG #(.DATAW(DATAW)) 
    rega(.clk(clk),
         .in(w1),
         .out(data1),
         .reset(reset));
         
REG #(.DATAW(DATAW)) 
    regb(.clk(clk),
         .in(data1),
         .out(out),
         .reset(reset));
         
round #(.DATAW(DATAW)) 
    roundd(.L(data1),
           .R(out),
           .C(C),
           .out(w4));
           
endmodule

