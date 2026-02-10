#include <gtest/gtest.h>
#include "math_utils.h"

TEST(FactorialTest, SmallValues) {
    EXPECT_EQ(math_utils::factorial(1), 1);
    EXPECT_EQ(math_utils::factorial(5), 120);
    EXPECT_EQ(math_utils::factorial(10), 3628800);
}

TEST(FibonacciTest, SmallValues) {
    EXPECT_EQ(math_utils::fibonacci(2), 1);
    EXPECT_EQ(math_utils::fibonacci(6), 8);
    EXPECT_EQ(math_utils::fibonacci(10), 55);
}
