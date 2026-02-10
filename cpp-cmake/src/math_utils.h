#pragma once

#include <cstdint>
#include <stdexcept>
#include <vector>

namespace math_utils {

/// Computes factorial of n.
/// Untested edge cases: n = 0, large n causing overflow, negative n.
uint64_t factorial(int n);

/// Computes the nth Fibonacci number (0-indexed).
/// Untested edge cases: n = 0, n = 1, large n, negative n.
uint64_t fibonacci(int n);

/// Checks whether n is a prime number.
/// Untested: no tests at all. Edge cases: 0, 1, 2, negative numbers,
/// large primes, even numbers.
bool is_prime(int n);

/// Returns all prime factors of n in ascending order.
/// Untested: no tests at all. Edge cases: n <= 1, n = 2, perfect squares,
/// large primes.
std::vector<int> prime_factors(int n);

} // namespace math_utils
