#include "math_utils.h"

namespace math_utils {

uint64_t factorial(int n) {
    if (n < 0) {
        throw std::invalid_argument("factorial: negative input");
    }
    uint64_t result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= static_cast<uint64_t>(i);
    }
    return result;
}

uint64_t fibonacci(int n) {
    if (n < 0) {
        throw std::invalid_argument("fibonacci: negative input");
    }
    if (n == 0) return 0;
    if (n == 1) return 1;

    uint64_t a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        uint64_t temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

bool is_prime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;

    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
    }
    return true;
}

std::vector<int> prime_factors(int n) {
    std::vector<int> factors;
    if (n <= 1) return factors;

    while (n % 2 == 0) {
        factors.push_back(2);
        n /= 2;
    }
    for (int i = 3; i * i <= n; i += 2) {
        while (n % i == 0) {
            factors.push_back(i);
            n /= i;
        }
    }
    if (n > 1) {
        factors.push_back(n);
    }
    return factors;
}

} // namespace math_utils
