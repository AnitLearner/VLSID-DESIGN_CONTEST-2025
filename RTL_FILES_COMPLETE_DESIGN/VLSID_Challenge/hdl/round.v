`timescale 1ns / 1ps

module round #(parameter DATAW=10)
              (input [(DATAW-1):0]L,
               input [(DATAW-1):0]R,
               input [(DATAW-1):0]C,
               output [(DATAW-1):0]out);
               
wire [(DATAW-1):0]w1,w2,w3,w4,w5;

lshift#(.DATAW(DATAW),
         .SHIFT(5)) 
  shift5(.in(L),
         .out(w1));
 
lshift #(.DATAW(DATAW),
         .SHIFT(1)) 
  shift1(.in(L),
         .out(w2));

assign w3 = L & w1;
assign w4 = R ^ w3;
assign w5 = w2 ^ w4;
assign out = C ^ w5;


endmodule
