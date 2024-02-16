#include <iostream>
#include <array>
#include <Eigen/Dense>
#include <cmath>
//#include <SDL.h>

using Eigen::Vector2f;

// Simulation Constants

const Vector2f boundsSize {1080, 1920};
const float damping {1.f};
const int particleNumber {100};
float particleSize {10.f};
float particleSpacing {1.f};




float sign(float value) {
    return static_cast<float>((value > 0) - (value < 0));
}

void resolveBoundaryCollisions(Vector2f &position, Vector2f &velocity, float& particleSize) {
    Vector2f halfBoundsSize = boundsSize / 2 - particleSize * Vector2f::Ones();

    if (std::abs(position.x()) > halfBoundsSize.x()) {
        position.x() = halfBoundsSize.x() * sign(position.x());
        velocity.x() *= -1 * damping;
    }

    if (std::abs(position.y()) > halfBoundsSize.y()) {
        position.y() = halfBoundsSize.y() * sign(position.y());
        velocity.y() *= -1 * damping;
    }

}


void start() {
    std::array<Vector2f, particleNumber> positions {};
    std::array<Vector2f, particleNumber> velocities {};

    int particlesPerRow = static_cast<int>(std::sqrt(particleNumber));
    int particlesPerCol = (particleNumber - 1) / particlesPerRow + 1;
    float spacing = particleSize*2 + particleSpacing;

    for (int i = 0; i < particleNumber; i++) {
        float x = (i % particlesPerRow - particlesPerRow / 2.f + 0.5f) * spacing;
        float y = (i / particlesPerRow - particlesPerRow / 2.f + 0.5f) * spacing;
        positions[i] = {x, y};
    }
}

void update(float deltaT) {
    for (int i {0}; i< std::size(positions); i++) {
        positions[i] = positions[i] + velocities[i] * deltaT;

        resolveBoundaryCollisions(positions[i], velocities[i], particleSize);
    }
}

