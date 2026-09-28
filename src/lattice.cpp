#include "lattice.hpp"

#include <numeric>

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
  for (int i = 0; i < this->rank; i++) {
    this->basis[i].resize(this->dim);

  generate_basis_vector:
    for (int j = 0; j < dim; j++) this->basis[i][j] = distr(gen);

    // check linear independence against preceeding vectors
    for (int k = i - 1; k >= 0; k--) {
      bool li = this->checkLinearIndependence(this->basis[i], this->basis[k]);
      if (!li) goto generate_basis_vector;
    }
  }
  return;
}

void Lattice::printMatrix(vector<vector<real_t>>& M) {
  cout << "rows: " << M.size() << " columns: " << M[0].size() << "\n";
  for (int i = 0; i < M.size(); i++) {
    for (int j = 0; j < M[i].size(); j++) cout << M[i][j] << " ";
    cout << "\n";
  }
}

void Lattice::printBasis() { printMatrix(this->basis); }

bool Lattice::checkLinearIndependence(vector<real_t> v, vector<real_t> w) {
  real_t ratio = v[0] / w[0];
  for (int i = 1; i < this->dim; i++) {
    real_t new_ratio = v[i] / w[i];
    if (!cmpDouble(ratio, new_ratio)) return true;
  }
  return false;
}

real_t Lattice::getL2Norm(vector<real_t> v) {
  real_t squared_norm = 0;

  for (const auto& x : v) squared_norm += x * x;

  return sqrt(squared_norm);
}

real_t Lattice::getBaseVolumeUpperBound() {
  real_t upper_bound = 1;
  for (const auto& v : this->basis) upper_bound *= getL2Norm(v);

  return upper_bound;
}

/*
 * LUP decomposition based on cormen's pseudocode
 *
 * return the number of swaps
 */
int Lattice::makeLUPDecompostion(vector<vector<real_t>>& A,
                                 vector<vector<real_t>>& LU, vector<int>& P) {
  real_t max;
  int max_idx, swap_count = 0;

  LU.resize(this->rank);
  P.resize(this->rank);

  // fill permutation matrix and copy A to LU
  for (int i = 0; i < this->rank; i++) {
    P[i] = i;
    LU[i] = A[i];  // deep copy apparently
  }

  for (int k = 0; k < this->rank; k++) {
    // find max on column k from the kth row forwards
    max = abs(LU[k][k]);
    max_idx = k;
    for (int i = k; i < this->rank; i++) {
      if (abs(LU[i][k]) > max) {
        max = abs(LU[i][k]);
        max_idx = i;
      }
    }

    // shoudlnt happen
    if (cmpDouble(max, 0)) return 0;

    // exchange row k with row max_idx in the permutation matrix
    std::swap(P[k], P[max_idx]);

    // exchange row k with row max_idx in the LU matrix
    std::swap(LU[k], LU[max_idx]);

    if (k != max_idx) swap_count++;

    for (int i = k + 1; i < this->rank; i++) {
      LU[i][k] = LU[i][k] / LU[k][k];
      for (int j = k + 1; j < this->rank; j++) {
        LU[i][j] -= LU[i][k] * LU[k][j];
      }
    }
  }

  return swap_count;
}

real_t Lattice::getBaseVolume() {
  int swaps;

  // perform LUP decomp
  swaps = this->makeLUPDecompostion(this->basis, this->LU, this->P);

  // compute the determinant by using the decomp
  real_t det = swaps % 2 == 0 ? 1 : -1;
  for (int i = 0; i < this->rank; i++) det *= this->LU[i][i];

  return det;
}

real_t Lattice::getHadamardRatio() {
  real_t volume_upper_bound = this->getBaseVolumeUpperBound();
  real_t volume = this->getBaseVolume();

  return volume / volume_upper_bound;
}
