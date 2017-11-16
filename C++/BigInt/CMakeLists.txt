cmake_minimum_required (VERSION 2.6)
project (BigInt_test CXX)

if (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pedantic -Wall")
endif()

add_library(BigInt BigInt.cpp)
add_executable(BigInt_test BigIntTest.cpp)
target_link_libraries(BigInt_test BigInt)
