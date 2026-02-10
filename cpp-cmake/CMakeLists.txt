cmake_minimum_required(VERSION 3.14)
project(cpp-cmake VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Main library
add_library(math_utils src/math_utils.cpp)
target_include_directories(math_utils PUBLIC src)

# Tests
enable_testing()
find_package(GTest REQUIRED)

add_executable(test_math tests/test_math.cpp)
target_link_libraries(test_math PRIVATE math_utils GTest::GTest GTest::Main)

include(GoogleTest)
gtest_discover_tests(test_math)
