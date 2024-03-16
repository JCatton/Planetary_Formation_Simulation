//
// Created by jonte on 16/02/2024.
//
#include <algorithm>
#include <array>
#include <Eigen/Dense>
#include <iostream>
#include "Constants.h"
#include "PointCalculations.h"

using Constants::vector2;
using std::array;

const vector2 UnitX{1, 0};
const vector2 UnitY{0, 1};
const real_t mass{10};

static real_t SmoothingKernel(const real_t radius, const real_t dst) {

    static const auto reference_zero = static_cast<real_t>(0);

    if (dst > radius) return reference_zero;

    // Sharp Peak Kernel
    real_t volume = (EIGEN_PI * std::pow(radius, 4)) / 6;
    return (radius - dst) * (radius - dst) / volume;

//    Smooth Peak Kernel
//    real_t volume = EIGEN_PI * std::pow(radius, 8) / 4;
//    real_t value = std::max(reference_zero, radius * radius - dst * dst);
//    return value * value * value / volume;
}

static real_t SmoothingKernelDerivative(const real_t radius, const real_t dst) {
    static const auto reference_zero = static_cast<real_t>(0);
    static const auto reference_24 = static_cast<real_t>(24);
    static const auto reference_12 = static_cast<real_t>(12);
    static const auto pi = static_cast<real_t>(EIGEN_PI);

    if (dst >= radius) {
        return reference_zero;
    }
//    Sharp Peak Kernel
    float scale = reference_12 / (std::pow(radius, 4) * EIGEN_PI);
    return (dst - radius) * scale;

//    Smooth Peak Kernel
//    real_t f = radius * radius - dst * dst;
//    real_t scale = -reference_24 / (pi * std::pow(radius, 8.f));
//    return scale * dst * f * f;
}

real_t CalculateDensity(
        const vector2 &samplePoint,
        const array<vector2, Constants::particleNumber> &positions) {
    real_t density = 0.f;
    const real_t mass = 1.f;

    for (const auto &position: positions) {
        real_t dst = (position - samplePoint).norm();
        real_t influence = SmoothingKernel(Constants::smoothingRadius, dst);
        density += mass * influence;
    }

    return density;
}

vector2 CalculateDensityGradient(
        const vector2 &samplePoint,
        const array<vector2, Constants::particleNumber> &positions,
        const array<real_t, Constants::particleNumber> &particleProperty) {
    // Currently doesn't do much due to every particle having identical mass. May be updated in the future.
    static const auto stepSize = static_cast<real_t>(0.001);

    vector2 propertyGradient = vector2{0.f, 0.f};
    for (int i{0}; i <= Constants::maxIter; i++) {
        if (positions[i] == samplePoint) {
            continue;
        }
        real_t dst = (positions[i] - samplePoint).norm();
        vector2 dir = (positions[i] - samplePoint) / dst;
        real_t slope = SmoothingKernelDerivative(Constants::smoothingRadius, dst);
        propertyGradient += -dir * slope * mass;
    }

    return propertyGradient;
}

real_t CalculateProperty(
        const vector2 &samplePoint,
        const array<vector2, Constants::particleNumber> &positions,
        const array<real_t, Constants::particleNumber> &particleProperty) {
    real_t property{0.f};

    for (int i{0}; i <= Constants::maxIter; i++) {
        if (positions[i] == samplePoint) {
            continue;
        }
        real_t dst = (positions[i] - samplePoint).norm();
        real_t influence = SmoothingKernel(Constants::smoothingRadius, dst);
        real_t density = CalculateDensity(samplePoint, positions);
        property += particleProperty[i] * influence * mass / density;
    }

    return property;
}


vector2 CalculatePropertyGradient(
        const vector2 &samplePoint,
        const array<vector2, Constants::particleNumber> &positions,
        const array<real_t, Constants::particleNumber> &particleProperty,
        array<real_t, Constants::particleNumber> densities) {
    static const auto stepSize = static_cast<real_t>(0.001);

    vector2 propertyGradient = vector2{0.f, 0.f};
    for (int i{0}; i <= Constants::maxIter; i++) {
        if (positions[i] == samplePoint) {
            continue;
        }
        real_t dst = (positions[i] - samplePoint).norm();
        vector2 dir = (positions[i] - samplePoint) / dst;
        real_t slope = SmoothingKernelDerivative(Constants::smoothingRadius, dst);
        real_t density = densities[i];
        propertyGradient += -particleProperty[i] * dir * slope * mass / density;
    }

    return propertyGradient;
}

real_t ConvertDensityToPressure(real_t density) {
    real_t densityError = density - Constants::targetDensity;
    real_t pressure = densityError * Constants::pressureMultiplier;

    return pressure;
}

vector2 CalculatePressureForce(
        const vector2 &samplePoint,
        const array<vector2, Constants::particleNumber> &positions,
        array<real_t, Constants::particleNumber> densities) {
    static const auto stepSize = static_cast<real_t>(0.001);

    vector2 propertyGradient = vector2{0.f, 0.f};
    for (int i{0}; i <= Constants::maxIter; i++) {
        if (positions[i] == samplePoint) {
            continue;
        }
        real_t dst = (positions[i] - samplePoint).norm();
        if (dst == 0) {
            std::cout << "Distance is zero" << positions[i] << " - " << samplePoint;
        }
        vector2 dir = (positions[i] - samplePoint) / dst;
        real_t slope = SmoothingKernelDerivative(Constants::smoothingRadius, dst);
        real_t density = densities[i];
        propertyGradient += -ConvertDensityToPressure(density) * dir * slope * mass / density;
    }

    return propertyGradient;
}
