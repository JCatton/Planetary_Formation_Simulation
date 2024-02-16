//
// Created by jonte on 16/02/2024.
//
#include <algorithm>
#include <array>
#include "PointCalculations.h"
#include "Constants.h"
#include <Eigen/Dense>

using Eigen::Vector2f;

static float SmoothingKernel(float radius, float dst) {
    float volume = EIGEN_PI * std::pow(radius, 8) / 4;
    float value = std::max(0.f, radius * radius - dst * dst);
    return value * value * value / volume;
}

float CalculateDensity(const Vector2f& samplePoint, const std::array<Vector2f, Constants::particleNumber>& positions) {
    float density = 0.f;
    const float mass = 1.f;

    for (const auto& position: positions) {
        float dst = (position - samplePoint).norm();
        float influence = SmoothingKernel(Constants::smoothingRadius, dst);
        density += mass * influence;
    }
}


