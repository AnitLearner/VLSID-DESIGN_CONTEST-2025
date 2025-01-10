/*
 * decision_tree.h
 *
 *  Created on: 04-Dec-2024
 *      Author: Piyush Tewari
 */

#ifndef DECISION_TREE_H_
#define DECISION_TREE_H_

#include "hls/ap_fixpt.hpp"
#include "hls/ap_int.hpp"

// Fixed-point type definitions
typedef hls::ap_uint<7> ap_nodes;                // Number of nodes (7-bit unsigned)
typedef hls::ap_uint<7> ap_leaves;               // Number of leaves (7-bit unsigned)
typedef hls::ap_int<8> ap_children;              // Children array elements (8-bit signed)
typedef hls::ap_int<5> ap_feature_split;         // Feature split (5-bit signed)
typedef hls::ap_fixpt<9, 7> ap_threshold;        // Threshold (9 bits: 7 integer, 1 fractional, 1 sign)
typedef hls::ap_uint<3> ap_value;                // Class value (3-bit unsigned)
typedef hls::ap_int<8> ap_parent;                // Parent nodes (8-bit signed)

// Input feature definition
struct ap_input_features {
    hls::ap_uint<1> f0;
    hls::ap_uint<1> f1;
    hls::ap_uint<1> f2;
    hls::ap_uint<1> f3;
    hls::ap_uint<1> f4;
    hls::ap_uint<10> f5;
    hls::ap_uint<10> f6;
    hls::ap_int<7> f7;

    // indexing according to case
    hls::ap_fixpt<10, 10> operator[](int idx) const {
        switch (idx) {
            case 0: return f0;
            case 1: return f1;
            case 2: return f2;
            case 3: return f3;
            case 4: return f4;
            case 5: return f5;
            case 6: return f6;
            case 7: return f7;
            default: return 0;
        }
    }
};

// Decision tree parameters
constexpr int NUM_NODES = 81;
constexpr int NUM_LEAVES = 41;

// Function prototype
ap_value decision_tree(const ap_input_features x);

#endif /* DECISION_TREE_H_ */
