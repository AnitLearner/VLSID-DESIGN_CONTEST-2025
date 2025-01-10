
module led_glower(  input [2:0]output_val,
                    output reg led_0,
                    output reg led_1,
                    output reg led_2 );

always @ (output_val)
begin
    case(output_val)
        3'b000:                 //This is case 1
        begin
            led_0 = 1;          //to glow this LED
            led_1 = 0;      
            led_2 = 0;
        end
        3'b001:                 //This is case 2
        begin
            led_0 = 0;         
            led_1 = 1;      
            led_2 = 0;
        end
        3'b010:                 //This is case 3
        begin
            led_0 = 1;         
            led_1 = 1;      
            led_2 = 0;
        end
        3'b011:                 //This is case 4
        begin
            led_0 = 0;          
            led_1 = 0;      
            led_2 = 1;
        end
        3'b100:                 //This is case 5
        begin
            led_0 = 1;         
            led_1 = 0;      
            led_2 = 1;
        end
        default:
        begin
            led_0 = 1;          
            led_1 = 1;      
            led_2 = 1;
        end
    endcase
end

endmodule

