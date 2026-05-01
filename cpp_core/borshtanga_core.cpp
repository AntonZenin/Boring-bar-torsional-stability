#include "borshtanga_core.hpp"
#include <cmath>


Complex computeDeltaHat(const BorshtangaParams& params, double omega) {
    double lambda1 = std::sqrt(params.rho * params.G) * params.Jp / params.Jr;
    double lambda2 = params.L * std::sqrt(params.rho / params.G);

    
    Complex p(0.0, omega);

    
    Complex one(1.0, 0.0);  
    Complex sqrtTerm = std::sqrt(one + params.delta1 * p);

    
    Complex argCoth = lambda2 * p / sqrtTerm;

    
    Complex cothValue = std::cosh(argCoth) / std::sinh(argCoth);

    
    Complex result = -p * lambda1 * sqrtTerm * cothValue;

    return result;
}


std::vector<std::pair<double, double>> buildDCurve(
    const BorshtangaParams& params,
    double omegaMin,
    double omegaMax,
    int numPoints
) {
    std::vector<std::pair<double, double>> curve;
    curve.reserve(numPoints);  

    
    double step = (omegaMax - omegaMin) / (numPoints - 1);

    for (int i = 0; i < numPoints; ++i) {
        double omega = omegaMin + i * step;

        
        if (std::abs(omega) < 1e-9) continue;

        Complex deltaHat = computeDeltaHat(params, omega);

    
        curve.push_back({deltaHat.real(), deltaHat.imag()});
    }

    return curve;
}