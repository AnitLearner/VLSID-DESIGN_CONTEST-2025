
module uart_control_signals(input clk,
                    input [2:0]output_value,
                    output [7:0]transmit_output,
                    output [2:0]led_transmit,
                    input rxrdy,
                    input [7:0]input_data,
                    output [31:0]receive_input,
                    output start,
                    input reset_decrypt,
                    input finish,
                    input ready,
                    output wen,
                    output start_dec,
                    output oen,
                    output [12:0]baud_val,
                    output [2:0]baud_val_frac,
                    output reset_n,
                    input button);

reg [2:0] wait_counter = 0;
reg reset_n_reg = 1;
reg initial_reset = 0;
reg oen_reg = 1;
reg [31:0]input_data_reg = 0;
reg [31:0]packet_data_reg = 0;                            
reg [1:0]counter_4 = 0;
reg start_reg = 0;
reg wen_reg = 1;
reg start_dec_reg = 0;
reg [2:0]transmit_output_reg=7; 

assign reset_n = reset_n_reg;
assign baud_val = 13'd26;
assign baud_val_frac = 3'b001;
assign oen = oen_reg;
assign start_dec = start_dec_reg;
assign wen = wen_reg;
assign start = start_reg;                          
assign transmit_output = {5'b0,transmit_output_reg}; //this is the output result, which will go transmit output, note LSB has output
assign led_transmit = transmit_output_reg;
assign receive_input = input_data_reg;

always @ (posedge clk)
begin
    if (button)
    begin
        wait_counter <= 0;
        reset_n_reg <= 1;
        initial_reset <= 0;
        oen_reg <= 1;
        input_data_reg <= 0;
        packet_data_reg <= 0;                            
        counter_4 <= 0;
        start_reg <= 0;
        wen_reg <= 1;
        start_dec_reg <= 0;
        transmit_output_reg <= 7; 
    end
    else
    begin
        if (initial_reset == 0)
        begin
            reset_n_reg <= 0;
            initial_reset <= 1;
        end
        else
        begin
            reset_n_reg <= 1;
        end
        
        if (rxrdy && oen_reg)
        begin
            if (counter_4 == 2'd3)
            begin
                input_data_reg <= {packet_data_reg[23:0],input_data};
                counter_4 <= 0;
                start_dec_reg <= 1;
            end
            else
            begin
                counter_4 <= counter_4 + 1;
                packet_data_reg[7:0] <= input_data;  //big endian format used, first 8 bits of lsb will come
                packet_data_reg[15:8] <= packet_data_reg[7:0];
                packet_data_reg[23:16] <= packet_data_reg[15:8];
                packet_data_reg[31:24] <= packet_data_reg[23:16];
            end
            oen_reg <= 0;
            wait_counter <= 0;
        end
        else
        begin
            start_dec_reg <= 0;
            if (wait_counter == 3)
            begin
                oen_reg <= 1;
                wait_counter <= 3;
            end
            else
            begin
                wait_counter <= wait_counter+1;
                oen_reg <= 0;
            end
        end
        
        if (reset_decrypt)
        begin
            start_reg <= 1'b1;
        end
        if (ready == 0)
        begin
            start_reg <= 1'b0;
        end
        
        if(finish)
        begin
            transmit_output_reg <= output_value;
            wen_reg <= 0;
        end
        else
        begin
            wen_reg <= 1;
        end
    end
end

endmodule

