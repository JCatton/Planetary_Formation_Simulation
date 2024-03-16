//
// Created by jonte on 16/02/2024.
//

#ifndef PLANETARY_FORMATION_SIMULATION_CONSTANTS_H
#define PLANETARY_FORMATION_SIMULATION_CONSTANTS_H

typedef double real_t;



namespace Constants {
    const real_t boundsSize[2] {100, 100};
    const real_t damping {0.5};
    const int particleNumber {100};
    const real_t particleSize {1};
    const real_t particleSpacing {1};
    const real_t smoothingRadius {10};
    const real_t particleMass{100};

    const real_t targetDensity{1};
    const real_t pressureMultiplier{5};

    const int maxIter {1000};

    using vector2 = typename std::conditional<std::is_same<real_t, double>::value, Eigen::Vector2d, Eigen::Vector2f>::type;
}


#endif //PLANETARY_FORMATION_SIMULATION_CONSTANTS_H
