#include "common.hpp"
#include "lattice.hpp"

int main() {
  Lattice L(2, 2);

  L.generateRandomBasis(1.0);
  L.printBasis();

  real_t hadamard_ratio = L.getHadamardRatio();

  cout << "Hadamard Ratio: " << hadamard_ratio << "\n";

  return 0;
}
