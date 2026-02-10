package com.example;

/**
 * Basic arithmetic calculator with untested edge cases.
 */
public class Calculator {

    /**
     * Adds two integers. Untested: integer overflow.
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * Subtracts b from a. Untested: integer underflow.
     */
    public int subtract(int a, int b) {
        return a - b;
    }

    /**
     * Divides a by b. Untested: division by zero, negative divisors,
     * integer truncation (e.g., 7 / 2 = 3).
     */
    public int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return a / b;
    }

    /**
     * Returns the factorial of n. Untested: negative input, n = 0,
     * large values that cause overflow.
     */
    public long factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Negative input: " + n);
        }
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * Returns the greatest common divisor of a and b.
     * Untested: no tests at all. Edge cases: zero inputs, negative inputs.
     */
    public int gcd(int a, int b) {
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
}
