#include "lattice.hpp"
#include "utils.hpp"

Lattice::Lattice(int dim, int rank) {
  this->dim = dim;
  this->rank = rank;
}

/*
 * interval - defines the interval of the coefficients of the basis
 * Requires dim and rank to be filled
 */
void Lattice::generateRandomBasis(double interval) {
  // get random number generator
  random_device rd;
  mt19937 gen(rd());
  uniform_real_distribution<double> distr(-interval, interval);

  // generate random basis
  this->basis.resize(this->rank);
  for (int i=0; i < this->rank; i++) {
    this->basis[i].resize(this->dim);

generate_basis_vector:
    for (int j = 0; j < dim; j++) 
      this->basis[i][j] = distr(gen);            

    // check linear independence against preceeding vectors
    for (int k = i-1; k >= 0; k--) {
      bool li = this->checkLinearIndependence(this->basis[i], this->basis[k]);
      if (!li) goto generate_basis_vector;
    }
  }
  return;  
}

void Lattice::printBasis() {
  for (int i = 0; i < this->rank; i++) {
    for (int j = 0; j < this->dim; j++)
      cout << this->basis[i][j] << " ";
    cout << "\n";
  }
}

bool Lattice::checkLinearIndependence(vector<double> v, vector<double> w) {
  double ratio = v[0] / w[0];
  for (int i = 1; i < this->dim; i++) {
    double new_ratio = v[i] / w[i]; 
    if (!cmpDouble(ratio, new_ratio))
      return true;
  }
  return false;
}

double Lattice::getHadamardRatio() {

}
