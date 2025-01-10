`timescale 1ns / 1ps

module decryption_top 
           (input clk,
           input [31:0] data_in,
           input income,
           output f0,
           output f1,
           output f2,
           output f3,
           output f4,
           output [9:0]f5,
           output [9:0]f6,
           output [6:0]f7,
           output save);
           
reg [63:0] masterkey = 64'h9c18a4b3d408eeb7;
wire kctr,dctr,set,lfsrset;
wire [15:0]distkey,distdata;
reg counter = 0;
        
FSM #(.DATAW(16))
    fsmdec(.clk(clk),
           .dctr(dctr),
           .kctr(kctr),
           .save(save),
           .set(set),
           .lfsrset(lfsrset),
           .Data(data_in),
           .Key(masterkey),
           .income(income),
           .dataout(distdata),
           .keyout(distkey));

decrypter #(.DATAW(16))
        dec(.clk(clk),
            .reset(set),
            .dctr(dctr),
            .kctr(kctr),
            .lfsrset(lfsrset),
            .plaindata({f0,f1,f2,f3,f4,f5,f6,f7}),
            .cipherdata(distdata),
            .key(distkey),
            .save(save));
endmodule