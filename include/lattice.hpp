#ifndef LATTICE_H
#define LATTICE_H

#include "common.hpp"
#include <vector> 
#include <random> 
#include <numeric> 
#include <algorithm> 

class Lattice {
  public:
    int dim;
    int rank;
    vector<vector<real_t>> basis;
    vector<vector<real_t>> LU;
    vector<int> P; // P[i] = j <=> theres a 1 in row i column j

    Lattice(int dim, int rank);

    void generateRandomBasis(double interval);
    void printBasis();
    void printMatrix(vector<vector<real_t>>& M);

    // linear algebra methods
    real_t getL2Norm(vector<real_t> v); 
    int makeLUPDecompostion(vector<vector<real_t>>& A, vector<vector<real_t>>& LU, vector<int>& P);
    bool checkLinearIndependence(vector<real_t> v, vector<real_t> w); 
    real_t getBaseVolumeUpperBound();
    real_t getBaseVolume();
    real_t getHadamardRatio();
};


#endif
