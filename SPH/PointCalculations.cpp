//
// Created by jonte on 16/02/2024.
//
#include <algorithm>
#include <array>
#include <Eigen/Dense>
#include "Constants.h"
#include "PointCalculations.h"

using Eigen::Vector2f;
using std::array;

const Vector2f UnitX {1, 0};
const Vector2f UnitY {0, 1};

static float SmoothingKernel(float radius, float dst) {
    float volume = EIGEN_PI * std::pow(radius, 8) / 4;
    float value = std::max(0.f, radius * radius - dst * dst);
    return value * value * value / volume;
}

static float SmoothingKernelDerivative(float radius, float dst) {
    if (dst >= radius) {
        return 0.f;
    }
    float f = radius * radius - dst * dst;
    float scale = -24 / (EIGEN_PI * std::pow(radius, 8));
    return scale * dst * f * f;
}

float CalculateDensity(const Vector2f& samplePoint, const array<Vector2f, Constants::particleNumber>& positions) {
    float density = 0.f;
    const float mass = 1.f;

    for (const auto& position: positions) {
        float dst = (position - samplePoint).norm();
        float influence = SmoothingKernel(Constants::smoothingRadius, dst);
        density += mass * influence;
    }

    return density;
}

float CalculateProperty(const Vector2f& samplePoint, const array<Vector2f, Constants::particleNumber>& positions, const array<float, Constants::particleNumber>& particleProperty) {
    float property {0.f};

    for (size_t i = 0; const auto& position: positions) {
        float dst = (position - samplePoint).norm();
        float influence = SmoothingKernel(Constants::smoothingRadius, dst);
        float density = CalculateDensity(samplePoint, positions);
        property += particleProperty[i] * influence * mass / density;
    }

    return property;
}


Vector2f CalculatePropertyGradient(Vector2f &samplePoint, const array<Vector2f, Constants::particleNumber>& positions, const array<float, Constants::particleNumber>& particleProperty) {
    const float stepSize = 0.001f;
    Vector2f propertyGradient = Vector2f {0.f, 0.f};
    for (size_t i = 0; const auto& position: positions) {
        float dst = (position - samplePoint).norm();
        Vector2f dir = (position - samplePoint) / dst;
        float slope = SmoothingKernelDerivative(smoothingRadius, dst);
        float density = CalculateDensity(position, positions);
        propertyGradient += particleProperty[i] * dir * slope * mass / density;
    }

    return propertyGradient;
}

