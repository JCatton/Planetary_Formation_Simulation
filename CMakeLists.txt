cmake_minimum_required(VERSION 3.27)
project(Planetary_Formation_Simulation)

set(CMAKE_CXX_STANDARD 20)

add_executable(Planetary_Formation_Simulation
        SPH/simulate.cpp
        SPH/PointCalculations.h
        SPH/PointCalculations.cpp
        SPH/Constants.h)

find_package(Eigen3 CONFIG REQUIRED)
target_link_libraries(Planetary_Formation_Simulation PRIVATE Eigen3::Eigen)