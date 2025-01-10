`timescale 1ns / 1ps


module lshift #(parameter DATAW=10, SHIFT = 5)
              (input [DATAW-1:0]in,
               output [DATAW-1:0]out);


assign out[(DATAW-1):SHIFT] = in[(DATAW-SHIFT-1):0];
assign out[(SHIFT-1):0]= in[(DATAW-1):(DATAW-SHIFT)];
endmodule
