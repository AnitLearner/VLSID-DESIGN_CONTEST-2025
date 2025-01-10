`timescale 1ns / 1ps

module keydegen #(parameter DATAW = 10)
               (input [(DATAW-1):0]key,
                input [(DATAW-1):0]k,
                output [(DATAW-1):0]out,
                input kctr,
                input clk,
                input reset
                );

wire [(DATAW-1):0] w1,w2,w3,w4,w5;

assign w5 = kctr?key:w4;

                        
REG #(.DATAW(DATAW)) 
    rega(.clk(clk),
         .in(w5),
         .out(out),
         .reset(reset));
         
REG #(.DATAW(DATAW)) 
    regb(.clk(clk),
         .in(out),
         .out(w1),
         .reset(reset));
         
REG #(.DATAW(DATAW)) 
    regr(.clk(clk),
         .in(w1),
         .out(w2),
         .reset(reset));

REG #(.DATAW(DATAW)) 
    reg1(.clk(clk),
         .in(w2),
         .out(w3),
         .reset(reset));
         
round #(.DATAW(DATAW)) 
    roundk(.L(out),
           .R(w3),
           .C(k),
           .out(w4));

endmodule