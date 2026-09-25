#ifndef LATTICE_H
#define LATTICE_H

#include "common.hpp"
#include <vector> 
#include <random> 
#include <numeric> 

class Lattice {
  public:
    int dim;
    int rank;
    vector<vector<double>> basis;

    void generateRandomBasis(double interval);
    void printBasis();
    bool checkLinearIndependence(vector<double> v, vector<double> w); 
    double getHadamardRatio();

    Lattice(int dim, int rank);
};


#endif
