# VLSID2025

**Securing and Accelerating Vehicle-to-Vehicle Communications to Combat Cyber-Threats and Enabling ML-Based Intelligent Decisions in Autonomous Vehicles**

---

## Table of Contents
1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Workflow](#workflow)
4. [Algorithms Involved](#algorithms-involved)
   - [Simeck Cipher](#simeck-cipher)
   - [Decision Tree](#decision-tree)

---

## Introduction

This project aims to implement a hardware-based encryption and decryption algorithm to secure vehicle-to-vehicle communication, suitable for higher levels of Advanced Driver Assistance Systems (ADAS) or Automated Driving. Additionally, a hardware ML accelerator has been developed to determine actionable decisions for autonomous vehicles. This accelerator processes input parameters such as relative position, velocity, and braking or turning intent from nearby vehicles to generate a decision.

---

## Key Features

- **Hardware Decryption**  
  The Simeck algorithm is implemented as a hardware decryptor using RTL design in Verilog. A detailed hardware architecture (attached separately) demonstrates its implementation.  

- **ML Accelerator**  
  Developed using the Microchip SmartHLS tool, this accelerator is based on the Decision Tree algorithm. Parameters such as leaf nodes, child nodes, and thresholds were extracted from a trained Python model.

- **Software Encryption**  
  The Simeck encryption algorithm is implemented using Python for secure data generation and transfer.

- **Web-Based Data Generation**  
  Using HTML, CSS, and Flask, a web-based application generates input datasets for the ML accelerator. The data is encrypted using Python before being transferred to the FPGA.

---

## Workflow

1. **Data Generation & Software Encryption**  
   A web-based application and Python scripts generate four input parameters: speed, relative distance, relative angle, and brake/turn intent (five distinct classes).  
   - **Speed Modeling**: Based on a log-normal distribution, inspired by research findings, to represent real-world conditions.  
   - **Relative Position**: Modeled using a normal distribution for natural positional variance.  
   - **Brake/Turn Intent**: Represents five predefined statuses to reflect distinct behaviors.  
   The generated data is encrypted using the Simeck algorithm in Python and transferred to the FPGA via UART protocol.

2. **Hardware Decryptor**  
   The encrypted data is received and decrypted using the same Simeck algorithm. This RTL-based implementation (in Verilog) prepares the data for the next stage.

3. **ML Accelerator**  
   The decrypted data is processed by the ML accelerator based on the Decision Tree algorithm.  
   - High-level synthesis (HLS) was employed using SmartHLS to create a C++ description of the model.  
   - A `.tcl` script was generated and used in Libero SoC to create a SmartDesign component.  
   - Five distinct output classes were defined for decision-making: Emergency Brake, Speed Up, Slow Down, Lane Change, and No Action.

---

## Algorithms Involved

### Simeck Cipher

1. **Input Specification**  
   - **Block Size**: The 32-bit plaintext is divided into two halves, L0 and R0, each 16 bits.  
   - **Key Size**: A 64-bit key is divided into subkeys for each encryption round.

2. **Feistel Structure**  
   - Utilizes a symmetric Feistel network.  
   - Each round processes one half of the data using a round function, followed by swapping.  
   - The process repeats for 31 rounds, producing a ciphertext by concatenating the final halves.

3. **Round Function**  
   - For each round:  
     - Compute Li+1 = Ri.  
     - Compute Ri+1 = Li ⊕ Ki, where:  
       - f(Ri) = (Ri & (Ri ≪ 5)) ⊕ (Ri ≪ 1).  
     - Ki represents the round key derived from the key schedule.

---

### Decision Tree

The Decision Tree algorithm is a classic supervised learning model that predicts outcomes based on hierarchical decisions.  

- **Structure**  
  - **Root Node**: Represents the entire dataset, serving as the starting point for splitting.  
  - **Internal Nodes**: Represent tests on dataset features, with branches leading to other nodes.  
  - **Leaf Nodes**: Represent final predictions or outcomes.  

- **Working**  
  - The root node splits the dataset based on the most significant feature using metrics like Gini impurity or information gain.  
  - Branches divide data subsets until meaningful groups are formed.  
  - Splitting continues until all instances in a node belong to the same class or a predefined depth is reached.

---


