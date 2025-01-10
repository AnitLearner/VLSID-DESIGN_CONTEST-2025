#This Tcl file sources other Tcl files to build the design(on which recursive export is run) in a bottom-up fashion

#Sourcing the Tcl file in which all the HDL source files used in the design are imported or linked
source hdl_source.tcl
build_design_hierarchy

#Sourcing the Tcl files in which HDL+ core definitions are created for HDL modules
source components/decision_tree_top.tcl 
source components/decryption_top.tcl 
build_design_hierarchy

#Sourcing the Tcl files for creating individual components under the top level
source components/COREUART_C0.tcl 
source components/VLSID_Challenge.tcl 
build_design_hierarchy
