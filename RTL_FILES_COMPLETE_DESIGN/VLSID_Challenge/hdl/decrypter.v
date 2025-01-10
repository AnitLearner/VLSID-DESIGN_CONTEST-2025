`timescale 1ns / 1ps

module decrypter #(parameter DATAW = 16)
                  (input clk,
                   input [DATAW-1:0] cipherdata,
                   input [DATAW-1:0] key,
                   input reset,
                   input dctr,
                   input kctr,
                   input save,
                   input lfsrset,
                   output reg [(2*DATAW-1):0]plaindata);
           
//wire [DATAW-1:0] w1,w2;
wire w3;
parameter num = 2**(DATAW)-4;
wire [(DATAW-1):0]data1,data2,w2,keyout;
assign w2 = num ^ w3;

always  @(posedge save)
begin
     plaindata[DATAW-1:0] <= data1;
     plaindata[(2*DATAW-1):DATAW] <= data2;
end

decrypt #(.DATAW(DATAW))
       dec1(.data(cipherdata),
            .C(keyout),
            .dctr(dctr),
            .clk(clk),
            .reset(reset),
            .out(data2),
            .data1(data1));
           
keydegen #(.DATAW(DATAW))
    enckey(.key(key),
           .k(w2),
           .kctr(kctr),
           .clk(clk),
           .reset(reset),
           .out(keyout));
        
 LFSR53 enclfsr(.set(lfsrset),
              .clk(clk),
              .out(w3));
 
endmodule
