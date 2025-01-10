#Importing and Linking all the HDL source files used in the design
import_files -library work -hdl_source hdl/debounce.v
import_files -library work -hdl_source hdl/led_glower.v
import_files -library work -hdl_source hdl/uart_control_signals.v
import_files -library work -hdl_source hdl/reg1.v
import_files -library work -hdl_source hdl/LFSR53.v
import_files -library work -hdl_source hdl/REG.v
import_files -library work -hdl_source hdl/lshift.v
import_files -library work -hdl_source hdl/round.v
import_files -library work -hdl_source hdl/decrypt.v
import_files -library work -hdl_source hdl/keydegen.v
import_files -library work -hdl_source hdl/decrypter.v
import_files -library work -hdl_source hdl/FSM.v
import_files -library work -hdl_source hdl/decryption_top.v
create_links -library work -hdl_source D:/ZICE/softconsole/finaldecision/hls_output/rtl/decisiontreefinal_decision_tree.v
