#include <iostream>
#include <array>
#include <Eigen/Dense>
#include <cmath>
#include <fstream>
#include "Constants.h"
#include "PointCalculations.h"

using Constants::vector2;
using std::array;

const vector2 boundsSize {Constants::boundsSize[0], Constants::boundsSize[1]};


float Sign(real_t value) {
    return static_cast<real_t>((value > 0) - (value < 0));
}

void ResolveBoundaryCollisions(vector2 &position, vector2 &velocity, real_t& particleSize) {
    vector2 halfBoundsSize = boundsSize / 2 - particleSize * vector2::Ones();

    if (std::abs(position.x()) > halfBoundsSize.x()) {
        position.x() = halfBoundsSize.x() * Sign(position.x());
        velocity.x() *= -1 * Constants::damping;
    }

    if (std::abs(position.y()) > halfBoundsSize.y()) {
        position.y() = halfBoundsSize.y() * Sign(position.y());
        velocity.y() *= -1 * Constants::damping;
    }

}

void SimulationStep(std::array<vector2, Constants::particleNumber> &positions, std::array<vector2, Constants::particleNumber> &velocities, real_t particleSize) {
    real_t deltaTime {0.1};

    // Generate and Populate Density Array
    array<real_t, Constants::particleNumber> densities = {};
    for (size_t i = 0; i < Constants::particleNumber; i++) {
        densities[i] = CalculateDensity(positions[i], positions);
    }

    // Calculate and Apply Pressure Forces
    for (size_t i = 0; const auto &position: positions) {
        vector2 pressureForce = CalculatePressureForce(position, positions, densities);
        vector2 pressureAcceleration = pressureForce / densities[i];
        velocities[i] += pressureAcceleration * deltaTime;
    }

    for (size_t i = 0; auto &position: positions) {
        position += velocities[i] * deltaTime;

        ResolveBoundaryCollisions(position, velocities[i], particleSize);
    }

}

void Plotter(std::array<vector2, Constants::particleNumber> &positions, const std::string &suffix) {
    std::string baseFilename {R"(C:\Users\jonte\CLionProjects\Planetary_Formation_Simulation\Position_Data)"};
    std::string extension {".txt"};
    std::string filename = baseFilename + "_" + suffix + extension;
    std::ofstream MyFile(filename);
    if (MyFile.is_open())
    {
        std::cout << "Greetings";
        for(auto position: positions){
            std::cout << "X position is: " << position.x() << std::endl;
            MyFile << position.x() << "," << position.y() << "\n";
        }
        MyFile.close();
    }
    else std::cout << "Unable to open file";
}


void Start() {
    std::array<vector2, Constants::particleNumber> positions {};
    std::array<vector2, Constants::particleNumber> velocities {};

    int particlesPerRow = static_cast<int>(std::sqrt(Constants::particleNumber));
    int particlesPerCol = static_cast<int>((Constants::particleNumber - 1) / particlesPerRow + 1);
    real_t spacing = Constants::particleSize*2 + Constants::particleSpacing;

    for (int i = 0; i < Constants::particleNumber; i++) {
        real_t x = (i % particlesPerRow - particlesPerRow / 2.f + 0.5f) * spacing;
        real_t y = (i / particlesPerRow - particlesPerCol / 2.f + 0.5f) * spacing;
        positions[i] = {x, y};
    }

    Plotter(positions, "initial");
    for (int i {0}; i <= Constants::maxIter; i++) {
        SimulationStep(positions, velocities, Constants::particleSize);
    }
    Plotter(positions, "final");
}

int main(int argc, char** argv) {
    std::cout << "Started";
    Start();
    std::cout << "Ended...";
}

//void update(float deltaT) {
//    for (int i {0}; i< std::size(positions); i++) {
//        positions[i] = positions[i] + velocities[i] * deltaT;
//
//        resolveBoundaryCollisions(positions[i], velocities[i], particleSize);
//    }
//}

