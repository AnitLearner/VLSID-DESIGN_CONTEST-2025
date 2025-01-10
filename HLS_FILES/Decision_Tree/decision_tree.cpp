/*
 * decision_tree.cpp
 *
 *  Created on: 04-Dec-2024
 *      Author: Piyush Tewari
 */

#include "decision_tree.h"

ap_value decision_tree(const ap_input_features x)
{
	#pragma HLS function top
    #pragma HLS memory partition argument(x)                   // to partition the input features
	#pragma HLS interface control type(simple)
	#pragma HLS memory partition variable(comparison)
    bool comparison[NUM_NODES];
	#pragma HLS memory partition variable(activation)
    bool activation[NUM_NODES];
	#pragma HLS memory partition variable(activation_leaf)
    bool activation_leaf[NUM_LEAVES];
	#pragma HLS memory partition variable(value_leaf)
    ap_value value_leaf[NUM_LEAVES];

    // Testbench parameters
	#pragma HLS memory partition variable(children_left)
    ap_children children_left[NUM_NODES] = {
        1, 2, 3, 4, 5, 6, 7, 8, -1, -1, -1, 12, -1, -1, 15, -1, -1, 18, 19, 20, 21,
        -1, -1, -1, -1, 26, -1, -1, 29, 30, 31, 32, 33, -1, -1, 36, -1, -1, -1, 40,
        41, 42, -1, -1, -1, 46, -1, -1, 49, -1, -1, 52, 53, 54, 55, 56, -1, -1, 59,
        60, -1, -1, -1, 64, -1, -1, -1, 68, 69, -1, -1, -1, 73, 74, -1, -1, 77, 78,
        -1, -1, -1
    };
	#pragma HLS memory partition variable(children_right)
    ap_children children_right[NUM_NODES] = {
        72, 51, 28, 17, 14, 11, 10, 9, -1, -1, -1, 13, -1, -1, 16, -1, -1, 25, 24,
        23, 22, -1, -1, -1, -1, 27, -1, -1, 48, 39, 38, 35, 34, -1, -1, 37, -1, -1,
        -1, 45, 44, 43, -1, -1, -1, 47, -1, -1, 50, -1, -1, 67, 66, 63, 58, 57, -1,
        -1, 62, 61, -1, -1, -1, 65, -1, -1, -1, 71, 70, -1, -1, -1, 76, 75, -1, -1,
        80, 79, -1, -1, -1
    };
	#pragma HLS memory partition variable(feature_split)
    ap_feature_split feature_split[NUM_NODES] = {
        0, 6, 5, 3, 1, 6, 5, 6, -2, -2, -2, 2, -2, -2, 5, -2, -2, 5, 6, 5, 5, -2,
        -2, -2, -2, 7, -2, -2, 4, 5, 2, 1, 7, -2, -2, 5, -2, -2, -2, 2, 7, 7, -2,
        -2, -2, 6, -2, -2, 5, -2, -2, 3, 6, 2, 5, 4, -2, -2, 5, 4, -2, -2, -2, 5,
        -2, -2, -2, 7, 7, -2, -2, -2, 6, 5, -2, -2, 6, 5, -2, -2, -2
    };
	#pragma HLS memory partition variable(threshold)
    ap_threshold threshold[NUM_NODES] = {
        0.5, 21.5, 39.5, 0.5, 0.5, 19.5, 18.5, 9.5, -2.0, -2.0, -2.0, 0.5, -2.0,
        -2.0, 28.5, -2.0, -2.0, 29.5, 15.0, 20.5, 17.0, -2.0, -2.0, -2.0, -2.0,
        31.0, -2.0, -2.0, 0.5, 50.5, 0.5, 0.5, 30.5, -2.0, -2.0, 43.5, -2.0, -2.0,
        -2.0, 0.5, 31.0, -30.5, -2.0, -2.0, -2.0, 18.5, -2.0, -2.0, 60.5, -2.0,
        -2.0, 0.5, 29.5, 0.5, 39.5, 0.5, -2.0, -2.0, 60.5, 0.5, -2.0, -2.0, -2.0,
        39.0, -2.0, -2.0, -2.0, 30.5, -30.5, -2.0, -2.0, -2.0, 14.5, 50.0, -2.0,
        -2.0, 19.5, 48.0, -2.0, -2.0, -2.0
    };
	#pragma HLS memory partition variable(value)
    ap_value value[NUM_NODES] = {
        1, 1, 2, 2, 2, 2, 2, 2, 0, 2, 2, 1, 1, 2, 4, 3, 4, 4, 4, 4, 0, 4, 0, 4, 3,
        3, 1, 3, 1, 1, 1, 3, 3, 1, 3, 4, 4, 4, 1, 0, 1, 1, 3, 1, 3, 0, 0, 1, 4, 4,
        1, 1, 1, 1, 1, 1, 4, 1, 4, 4, 1, 4, 1, 1, 2, 1, 1, 3, 1, 3, 1, 3, 4, 2, 2,
        0, 4, 4, 4, 0, 4
    };
	#pragma HLS memory partition variable(parent)
    ap_parent parent[NUM_NODES] = {
        -1, 0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 11, 11, 4, 14, 14, 3, 17, 18, 19, 20,
        20, 19, 18, 17, 25, 25, 2, 28, 29, 30, 31, 32, 32, 31, 35, 35, 30, 29, 39,
        40, 41, 41, 40, 39, 45, 45, 28, 48, 48, 1, 51, 52, 53, 54, 55, 55, 54, 58,
        59, 59, 58, 53, 63, 63, 52, 51, 67, 68, 68, 67, 0, 72, 73, 73, 72, 76, 77,
        77, 76
    };


    // Comparison logic
	#pragma HLS loop unroll
    for (int i = 0; i < NUM_NODES; i++) {
        if (feature_split[i] >= 0) {
            comparison[i] = x[feature_split[i]] <= threshold[i];
        } else {
            comparison[i] = true;  // Leaf nodes
        }
    }

    // Node activity logic
    int iLeaf = 0;
	#pragma HLS loop unroll
    for (int i = 0; i < NUM_NODES; i++) {
        if (i == 0) {  // Root node is always active
            activation[i] = true;
        } else if (i == children_left[parent[i]]) {
            activation[i] = comparison[parent[i]] && activation[parent[i]];
        } else {
            activation[i] = !comparison[parent[i]] && activation[parent[i]];
        }

        if (children_left[i] == -1) {  // Leaf node
            activation_leaf[iLeaf] = activation[i];
            value_leaf[iLeaf] = value[i];
            iLeaf++;
        }
    }

    // Find the activated leaf
	#pragma HLS loop unroll
    for (int i = 0; i < NUM_LEAVES; i++) {
        if (activation_leaf[i]) {
            return value_leaf[i];
        }
    }

    return 7;  // Default return in case of no match
}



