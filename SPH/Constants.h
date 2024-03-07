//
// Created by jonte on 16/02/2024.
//

#ifndef PLANETARY_FORMATION_SIMULATION_CONSTANTS_H
#define PLANETARY_FORMATION_SIMULATION_CONSTANTS_H

typedef double real_t;



namespace Constants {
    const real_t boundsSize[2] {1080, 1920};
    const real_t damping {1};
    const int particleNumber {100};
    const real_t particleSize {10};
    const real_t particleSpacing {1};
    const real_t smoothingRadius {20};
    const real_t particleMass {10};

    using vector2 = typename std::conditional<std::is_same<real_t, double>::value, Eigen::Vector2d, Eigen::Vector2f>::type;
}


#endif //PLANETARY_FORMATION_SIMULATION_CONSTANTS_H
