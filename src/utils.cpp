#include "utils.hpp"

bool cmpDouble(double a, double b) {
  double eps, diff, relative_eps;
  eps = numeric_limits<double>::epsilon();
  diff = abs(a - b);
  relative_eps = max(eps, max(abs(a), abs(b)) * eps);

  return diff < relative_eps;
}
