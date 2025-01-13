**Securing and Accelerating Vehicle-to-Vehicle communications to combat Cyber-Threats and enabling ML-Based Intelligent decision in autonomous Vehicles.**

**Introduction**
This project aims to implement a hardware based encryption and decryption algorithm to secure vehicle to vehicle communication which can be used in higher levels of ADAS or Automated Driving.
In addition to that, a hardware ML Accelerator has also been implemented which outputs a decision that should be taken by the car when it recieves the relative position, velocity and braking/turning intent from a car in its proximity.

**Algorithms Used**

**1. Simeck Algorithm**
For encryption and decryption , Simeck Algorithm has been used. It is a block cipher based on Fiestal Network Structure.
Reference: - https://cacr.uwaterloo.ca/techreports/2015/cacr2015-07.pdf

For demonstration purpose, the encryption of the data was done using a python script and the encrypted data was sent to the SoC (Polarfire Icicle Kit) using UART protocol.  The decyrption and ML processing was done on the FPGA of the SoC. 

**2. Decision Tree**
The ML model is based on Decision Tree Algorithm. The weights were trained using a python script on our custom dataset. The trained weights were then used in the HLS code to design the RTL structure of the
ML accelerator.



