//
// Created by jonte on 16/02/2024.
//

#ifndef PLANETARY_FORMATION_SIMULATION_POINTCALCULATIONS_H
#define PLANETARY_FORMATION_SIMULATION_POINTCALCULATIONS_H

#include <Eigen/Dense>
#include "Constants.h"

using Constants::vector2;
using std::array;

real_t CalculateDensity(const vector2 &samplePoint, const std::array<vector2, Constants::particleNumber> &positions);

vector2 CalculateDensityGradient(
        const vector2 &samplePoint, const array<vector2, Constants::particleNumber> &positions,
        const array<real_t, Constants::particleNumber> &particleProperty);

real_t CalculateProperty(
        const vector2 &samplePoint, const array<vector2, Constants::particleNumber> &positions,
        const array<real_t, Constants::particleNumber> &particleProperty);

vector2 CalculatePropertyGradient(
        const vector2 &samplePoint, const array<vector2, Constants::particleNumber> &positions,
        const array<real_t, Constants::particleNumber> &particleProperty);

vector2 CalculatePressureForce(
        const vector2 &samplePoint, const array<vector2, Constants::particleNumber> &positions,
        array<real_t, Constants::particleNumber> densities);

#endif //PLANETARY_FORMATION_SIMULATION_POINTCALCULATIONS_H
