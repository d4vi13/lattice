#include "common.hpp"
#include "lattice.hpp"

int main() {
  Lattice L(4, 4); 

  L.generateRandomBasis(100.0);
  L.printBasis();

  return 0;
}
