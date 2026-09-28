#include "utils.hpp"

bool cmpDouble(real_t a, real_t b) {
  real_t eps, diff, relative_eps;
  eps = numeric_limits<real_t>::epsilon();
  diff = abs(a - b);
  relative_eps = max(eps, max(abs(a), abs(b)) * eps);

  return diff < relative_eps;
}
