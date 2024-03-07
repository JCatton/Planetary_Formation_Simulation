#include <iostream>
#include <array>
#include <Eigen/Dense>
#include <cmath>
#include <fstream>
#include "Constants.h"

using Constants::vector2;

const vector2 boundsSize {Constants::boundsSize[0], Constants::boundsSize[1]};


float sign(float value) {
    return static_cast<float>((value > 0) - (value < 0));
}

void resolveBoundaryCollisions(vector2 &position, vector2 &velocity, real_t& particleSize) {
    vector2 halfBoundsSize = boundsSize / 2 - particleSize * vector2::Ones();

    if (std::abs(position.x()) > halfBoundsSize.x()) {
        position.x() = halfBoundsSize.x() * sign(position.x());
        velocity.x() *= -1 * Constants::damping;
    }

    if (std::abs(position.y()) > halfBoundsSize.y()) {
        position.y() = halfBoundsSize.y() * sign(position.y());
        velocity.y() *= -1 * Constants::damping;
    }

}

void plotter(std::array<vector2, Constants::particleNumber> &positions) {
    std::ofstream MyFile(R"(C:\Users\jonte\CLionProjects\Planetary_Formation_Simulation\Position_Data.txt)");
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


void start() {
    std::array<vector2, Constants::particleNumber> positions {};
    std::array<vector2, Constants::particleNumber> velocities {};

    int particlesPerRow = static_cast<int>(std::sqrt(Constants::particleNumber));
    int particlesPerCol = (Constants::particleNumber - 1) / particlesPerRow + 1;
    real_t spacing = Constants::particleSize*2 + Constants::particleSpacing;

    for (int i = 0; i < Constants::particleNumber; i++) {
        real_t x = (i % particlesPerRow - particlesPerRow / 2.f + 0.5f) * spacing;
        real_t y = (i / particlesPerRow - particlesPerCol / 2.f + 0.5f) * spacing;
        positions[i] = {x, y};
    }

    plotter(positions);
}

int main(int argc, char** argv) {
    std::cout << "Started";
    start();
    std::cout << "Ended...";
}

//void update(float deltaT) {
//    for (int i {0}; i< std::size(positions); i++) {
//        positions[i] = positions[i] + velocities[i] * deltaT;
//
//        resolveBoundaryCollisions(positions[i], velocities[i], particleSize);
//    }
//}

