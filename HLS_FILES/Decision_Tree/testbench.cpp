/*
 * testbench.cpp
 *
 *  Created on: 05-Dec-2024
 *      Author: Piyush Tewari
 */

#include "decision_tree.h"
#include <iostream>

int matches = 1; // Assume all inputs will match
ap_input_features x;

int main() {
    // Test inputs and expected outputs
    for (int i = 0; i < 50; i++) {
        // Assign the feature values based on the input test samples
        switch (i) {
          case 0: x = { 0, 1, 0, 0, 0, 30, 88, -12 }; break;
          case 1: x = { 0, 0, 1, 0, 0, 21, 78, -30 }; break;
          case 2: x = { 0, 0, 1, 0, 0, 65, 75, -48 }; break;
          case 3: x = { 0, 0, 0, 1, 0, 28, 3, 53 }; break;
          case 4: x = { 0, 0, 0, 0, 1, 53, 50, -17 }; break;
          case 5: x = { 0, 0, 0, 0, 1, 99, 92, -33 }; break;
          case 6: x = { 0, 0, 1, 0, 0, 26, 5, 45 }; break;
          case 7: x = { 0, 0, 1, 0, 0, 55, 87, 36 }; break;
          case 8: x = { 0, 0, 0, 1, 0, 25, 13, -34 }; break;
          case 9: x = { 1, 0, 0, 0, 0, 36, 65, 7 }; break;
          case 10: x = { 0, 0, 1, 0, 0, 60, 97, 47 }; break;
          case 11: x = { 1, 0, 0, 0, 0, 28, 20, 37 }; break;
          case 12: x = { 1, 0, 0, 0, 0, 45, 116, 33 }; break;
          case 13: x = { 0, 0, 0, 0, 1, 23, 36, 14 }; break;
          case 14: x = { 0, 0, 1, 0, 0, 31, 21, -21 }; break;
          case 15: x = { 1, 0, 0, 0, 0, 23, 70, -56 }; break;
          case 16: x = { 0, 0, 0, 1, 0, 21, 76, 58 }; break;
          case 17: x = { 0, 0, 0, 0, 1, 33, 38, 31 }; break;
          case 18: x = { 0, 0, 0, 0, 1, 25, 40, -27 }; break;
          case 19: x = { 1, 0, 0, 0, 0, 48, 25, 57 }; break;
          case 20: x = { 0, 1, 0, 0, 0, 30, 85, 32 }; break;
          case 21: x = { 0, 0, 0, 0, 1, 71, 111, 40 }; break;
          case 22: x = { 0, 0, 0, 0, 1, 38, 77, 38 }; break;
          case 23: x = { 0, 0, 0, 0, 1, 35, 98, -4 }; break;
          case 24: x = { 0, 0, 1, 0, 0, 35, 46, -58 }; break;
          case 25: x = { 0, 0, 1, 0, 0, 101, 79, 33 }; break;
          case 26: x = { 1, 0, 0, 0, 0, 43, 20, 41 }; break;
          case 27: x = { 0, 0, 1, 0, 0, 28, 17, -57 }; break;
          case 28: x = { 0, 0, 0, 0, 1, 24, 89, -1 }; break;
          case 29: x = { 0, 0, 1, 0, 0, 29, 124, -8 }; break;
          case 30: x = { 0, 0, 1, 0, 0, 51, 4, -18 }; break;
          case 31: x = { 1, 0, 0, 0, 0, 97, 103, -48 }; break;
          case 32: x = { 0, 0, 0, 1, 0, 55, 82, 8 }; break;
          case 33: x = { 0, 0, 0, 0, 1, 43, 77, -33 }; break;
          case 34: x = { 1, 0, 0, 0, 0, 77, 56, -17 }; break;
          case 35: x = { 1, 0, 0, 0, 0, 46, 60, 10 }; break;
          case 36: x = { 0, 0, 1, 0, 0, 21, 110, 49 }; break;
          case 37: x = { 0, 0, 0, 0, 1, 65, 105, -32 }; break;
          case 38: x = { 1, 0, 0, 0, 0, 25, 70, -14 }; break;
          case 39: x = { 0, 0, 0, 0, 1, 59, 31, 55 }; break;
          case 40: x = { 0, 0, 0, 0, 1, 35, 14, 53 }; break;
          case 41: x = { 0, 0, 0, 0, 1, 37, 47, -57 }; break;
          case 42: x = { 0, 0, 1, 0, 0, 34, 74, 27 }; break;
          case 43: x = { 0, 0, 0, 0, 1, 77, 112, -6 }; break;
          case 44: x = { 0, 0, 0, 0, 1, 64, 12, 20 }; break;
          case 45: x = { 0, 1, 0, 0, 0, 76, 60, -3 }; break;
          case 46: x = { 1, 0, 0, 0, 0, 27, 21, -42 }; break;
          case 47: x = { 0, 0, 0, 0, 1, 9, 120, -59 }; break;
          case 48: x = { 0, 0, 0, 0, 1, 49, 54, -7 }; break;
          case 49: x = { 0, 0, 0, 0, 1, 52, 65, -9 }; break;
        }
        ap_value result = decision_tree(x);
        int expected = 1; // Set the expected result for each case
        switch (i) {
          case 0: expected = { 1 }; break;
          case 1: expected = { 1 }; break;
          case 2: expected = { 1 }; break;
          case 3: expected = { 4 }; break;
          case 4: expected = { 1 }; break;
          case 5: expected = { 1 }; break;
          case 6: expected = { 2 }; break;
          case 7: expected = { 1 }; break;
          case 8: expected = { 4 }; break;
          case 9: expected = { 4 }; break;
          case 10: expected = { 1 }; break;
          case 11: expected = { 4 }; break;
          case 12: expected = { 4 }; break;
          case 13: expected = { 1 }; break;
          case 14: expected = { 2 }; break;
          case 15: expected = { 4 }; break;
          case 16: expected = { 3 }; break;
          case 17: expected = { 1 }; break;
          case 18: expected = { 1 }; break;
          case 19: expected = { 4 }; break;
          case 20: expected = { 1 }; break;
          case 21: expected = { 1 }; break;
          case 22: expected = { 1 }; break;
          case 23: expected = { 1 }; break;
          case 24: expected = { 1 }; break;
          case 25: expected = { 1 }; break;
          case 26: expected = { 4 }; break;
          case 27: expected = { 2 }; break;
          case 28: expected = { 1 }; break;
          case 29: expected = { 1 }; break;
          case 30: expected = { 0 }; break;
          case 31: expected = { 4 }; break;
          case 32: expected = { 1 }; break;
          case 33: expected = { 1 }; break;
          case 34: expected = { 4 }; break;
          case 35: expected = { 4 }; break;
          case 36: expected = { 1 }; break;
          case 37: expected = { 1 }; break;
          case 38: expected = { 4 }; break;
          case 39: expected = { 1 }; break;
          case 40: expected = { 2 }; break;
          case 41: expected = { 1 }; break;
          case 42: expected = { 1 }; break;
          case 43: expected = { 1 }; break;
          case 44: expected = { 1 }; break;
          case 45: expected = { 1 }; break;
          case 46: expected = { 4 }; break;
          case 47: expected = { 1 }; break;
          case 48: expected = { 1 }; break;
          case 49: expected = { 1 }; break;
        }

        if (result != expected) {
            std::cout << "Mismatch for input " << i + 1 << ": Expected " << expected << ", Got " << (int)result << std::endl;
            matches = 0;
        }
    }

    if (matches) {
        std::cout << "All inputs matched the expected outputs." << std::endl;
    } else {
        std::cout << "Some inputs did not match the expected outputs." << std::endl;
    }

    return 0;
}
