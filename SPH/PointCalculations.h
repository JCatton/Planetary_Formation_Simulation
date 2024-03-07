//
// Created by jonte on 16/02/2024.
//

#ifndef PLANETARY_FORMATION_SIMULATION_POINTCALCULATIONS_H
#define PLANETARY_FORMATION_SIMULATION_POINTCALCULATIONS_H
#include <Eigen/Dense>
#include "Constants.h"

using Constants::vector2;

real_t CalculateDensity(const vector2& samplePoint, const std::array<vector2, Constants::particleNumber>& positions);


#endif //PLANETARY_FORMATION_SIMULATION_POINTCALCULATIONS_H
