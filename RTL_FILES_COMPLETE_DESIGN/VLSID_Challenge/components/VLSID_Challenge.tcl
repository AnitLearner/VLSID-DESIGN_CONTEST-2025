# Creating SmartDesign "VLSID_Challenge"
set sd_name {VLSID_Challenge}
create_smartdesign -sd_name ${sd_name}

# Disable auto promotion of pins of type 'pad'
auto_promote_pad_pins -promote_all 0

# Create top level Scalar Ports
sd_create_scalar_port -sd_name ${sd_name} -port_name {RX} -port_direction {IN}
sd_create_scalar_port -sd_name ${sd_name} -port_name {clk} -port_direction {IN}
sd_create_scalar_port -sd_name ${sd_name} -port_name {input_button} -port_direction {IN}

sd_create_scalar_port -sd_name ${sd_name} -port_name {LED_0} -port_direction {OUT}
sd_create_scalar_port -sd_name ${sd_name} -port_name {LED_1} -port_direction {OUT}
sd_create_scalar_port -sd_name ${sd_name} -port_name {LED_2} -port_direction {OUT}
sd_create_scalar_port -sd_name ${sd_name} -port_name {LED_3} -port_direction {OUT}
sd_create_scalar_port -sd_name ${sd_name} -port_name {TX} -port_direction {OUT}
sd_create_scalar_port -sd_name ${sd_name} -port_name {outtest2} -port_direction {OUT}
sd_create_scalar_port -sd_name ${sd_name} -port_name {outtest} -port_direction {OUT}



sd_connect_pins_to_constant -sd_name ${sd_name} -pin_names {LED_3} -value {GND}
# Add COREUART_C0_0 instance
sd_instantiate_component -sd_name ${sd_name} -component_name {COREUART_C0} -instance_name {COREUART_C0_0}
sd_connect_pins_to_constant -sd_name ${sd_name} -pin_names {COREUART_C0_0:BIT8} -value {VCC}
sd_connect_pins_to_constant -sd_name ${sd_name} -pin_names {COREUART_C0_0:CSN} -value {GND}
sd_connect_pins_to_constant -sd_name ${sd_name} -pin_names {COREUART_C0_0:ODD_N_EVEN} -value {GND}
sd_mark_pins_unused -sd_name ${sd_name} -pin_names {COREUART_C0_0:OVERFLOW}
sd_connect_pins_to_constant -sd_name ${sd_name} -pin_names {COREUART_C0_0:PARITY_EN} -value {GND}
sd_mark_pins_unused -sd_name ${sd_name} -pin_names {COREUART_C0_0:PARITY_ERR}
sd_mark_pins_unused -sd_name ${sd_name} -pin_names {COREUART_C0_0:TXRDY}
sd_mark_pins_unused -sd_name ${sd_name} -pin_names {COREUART_C0_0:FRAMING_ERR}



# Add debounce_0 instance
sd_instantiate_hdl_module -sd_name ${sd_name} -hdl_module_name {debounce} -hdl_file {hdl\debounce.v} -instance_name {debounce_0}



# Add decision_tree_top_0 instance
sd_instantiate_hdl_core -sd_name ${sd_name} -hdl_core_name {decision_tree_top} -instance_name {decision_tree_top_0}



# Add decryption_top_0 instance
sd_instantiate_hdl_core -sd_name ${sd_name} -hdl_core_name {decryption_top} -instance_name {decryption_top_0}



# Add led_glower_0 instance
sd_instantiate_hdl_module -sd_name ${sd_name} -hdl_module_name {led_glower} -hdl_file {hdl\led_glower.v} -instance_name {led_glower_0}



# Add uart_control_signals_1 instance
sd_instantiate_hdl_module -sd_name ${sd_name} -hdl_module_name {uart_control_signals} -hdl_file {hdl\uart_control_signals.v} -instance_name {uart_control_signals_1}



# Add scalar net connections
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:CLK" "clk" "debounce_0:clk" "decision_tree_top_0:clk" "decryption_top_0:clk" "uart_control_signals_1:clk" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:OEN" "uart_control_signals_1:oen" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:RESET_N" "uart_control_signals_1:reset_n" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:RX" "RX" "outtest" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:RXRDY" "uart_control_signals_1:rxrdy" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:TX" "TX" "outtest2" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:WEN" "uart_control_signals_1:wen" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"LED_0" "led_glower_0:led_0" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"LED_1" "led_glower_0:led_1" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"LED_2" "led_glower_0:led_2" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"debounce_0:i" "input_button" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"debounce_0:o" "uart_control_signals_1:button" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:finish" "uart_control_signals_1:finish" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:ready" "uart_control_signals_1:ready" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:reset" "decryption_top_0:save" "uart_control_signals_1:reset_decrypt" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:start" "uart_control_signals_1:start" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f0_read_data" "decryption_top_0:f0" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f1_read_data" "decryption_top_0:f1" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f2_read_data" "decryption_top_0:f2" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f3_read_data" "decryption_top_0:f3" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f4_read_data" "decryption_top_0:f4" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decryption_top_0:income" "uart_control_signals_1:start_dec" }

# Add bus net connections
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:BAUD_VAL" "uart_control_signals_1:baud_val" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:BAUD_VAL_FRACTION" "uart_control_signals_1:baud_val_frac" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:DATA_IN" "uart_control_signals_1:transmit_output" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"COREUART_C0_0:DATA_OUT" "uart_control_signals_1:input_data" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:return_val" "uart_control_signals_1:output_value" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f5_read_data" "decryption_top_0:f5" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f6_read_data" "decryption_top_0:f6" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decision_tree_top_0:x_f7_read_data" "decryption_top_0:f7" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"decryption_top_0:data_in" "uart_control_signals_1:receive_input" }
sd_connect_pins -sd_name ${sd_name} -pin_names {"led_glower_0:output_val" "uart_control_signals_1:led_transmit" }


# Re-enable auto promotion of pins of type 'pad'
auto_promote_pad_pins -promote_all 1
# Save the SmartDesign 
save_smartdesign -sd_name ${sd_name}
# Generate SmartDesign "VLSID_Challenge"
generate_component -component_name ${sd_name}
