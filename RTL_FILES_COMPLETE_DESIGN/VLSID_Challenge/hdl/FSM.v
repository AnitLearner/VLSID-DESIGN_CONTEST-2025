`timescale 1ns / 1ps


module FSM #(parameter DATAW=10)
           (input clk,
           input  income,
           input [(2*DATAW-1):0] Data,
           input [(4*DATAW-1):0] Key,
           output reg [(DATAW-1):0]keyout,
           output reg [(DATAW-1):0]dataout,
           output reg dctr,
           output reg kctr,
           output reg save,
           output reg set,
           output reg lfsrset);


parameter s1 = 2'b00;
parameter s2 = 2'b01;
parameter s3 = 2'b10;
parameter s4 = 2'b11;

//reg [1:0] state;
reg [4:0] cycle_counter=0;
reg [1:0] state = s1;


always @(posedge clk)
begin

case (state)
    s1 : begin
       save<=1'b0;
       if (income)
       begin
          keyout <= Key[DATAW-1:0];
          state <= s2;
          dctr <= 1'b0;
          kctr <= 1'b1;
          set <=0;
          lfsrset<=1;
      
       end 
       else set <=1; 
    end
    
    s2 : begin
            cycle_counter <= cycle_counter + 1'b1;
        if(cycle_counter ==0)
        begin
            keyout <= Key[2*DATAW-1:DATAW];
        end
        if(cycle_counter ==1)
        begin
            keyout <= Key[3*DATAW-1:2*DATAW];
            dataout <= Data[DATAW-1:0];
            state <= s3;
            cycle_counter <= 0;
            dctr <= 1'b1;
            kctr <=1'b1;
            save <= 1'b0;
            set <=0;
        end
    end
    
    s3 : begin
            cycle_counter <= cycle_counter + 1'b1;
        if(cycle_counter ==0)
        begin
            dataout <= Data[2*DATAW-1:DATAW];
            keyout <= Key[4*DATAW-1:3*DATAW]; 
        end
        if(cycle_counter ==1)
        begin
            dataout <= Data[2*DATAW-1:DATAW];
            keyout <= Key[4*DATAW-1:3*DATAW];
            state <= s4;
            dctr <= 1'b0;
            kctr <=1'b0;
            set <=0;
            save<=0;
            cycle_counter <= 0;
            lfsrset<=0;
        end
    end
    s4 : begin
            cycle_counter <= cycle_counter + 1'b1;
        if(cycle_counter ==30)
        begin
            cycle_counter <= 0;
            save <=1'b1;
            lfsrset<=1;
            if (income)
            begin
                state <= s2;
                dctr <= 1'b0;
                kctr <= 1'b1;
                keyout <= Key[DATAW-1:0];
                set <=0;
            end
            else begin
                state <= s1;
                set <= 1;
                dctr <= 1'b0;
                kctr <= 1'b0;
            
            end
        end
    end
endcase

end  
endmodule