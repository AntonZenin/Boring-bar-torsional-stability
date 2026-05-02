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

    return -p * lambda1 * sqrtTerm * cothValue;
}

std::vector<std::pair<double, double>> buildDCurve(
    const BorshtangaParams& params,
    double omegaMin, double omegaMax, int numPoints
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

std::vector<DCurvePoint> buildDCurveWithHatching(
    const BorshtangaParams& params,
    double omegaMin, double omegaMax, int numPoints,
    double hatch_length, int hatch_step
) {
    std::vector<DCurvePoint> result;
    result.reserve(numPoints);

    double step = (omegaMax - omegaMin) / (numPoints - 1);

    
    std::vector<DCurvePoint> all_points;
    for (int i = 0; i < numPoints; ++i) {
        double omega = omegaMin + i * step;
        if (std::abs(omega) < 1e-9) continue;
        Complex d = computeDeltaHat(params, omega);
        DCurvePoint pt;
        pt.re = d.real();
        pt.im = d.imag();
        pt.hatch_dx = 0.0;
        pt.hatch_dy = 0.0;
        pt.omega = omega;
        all_points.push_back(pt);
    }

    
    for (size_t i = 0; i < all_points.size(); ++i) {
        if (i % hatch_step != 0) {
            result.push_back(all_points[i]);
            continue;
        }

        
        size_t i_next = (i + 1 < all_points.size()) ? i + 1 : i;
        size_t i_prev = (i > 0) ? i - 1 : i;

        double dx = all_points[i_next].re - all_points[i_prev].re;
        double dy = all_points[i_next].im - all_points[i_prev].im;

        
        double norm = std::sqrt(dx * dx + dy * dy);
        if (norm < 1e-12) {
            result.push_back(all_points[i]);
            continue;
        }
        dx /= norm;
        dy /= norm;

        
        double nx = -dy;
        double ny = dx;

        DCurvePoint pt = all_points[i];
        pt.hatch_dx = nx * hatch_length;
        pt.hatch_dy = ny * hatch_length;
        result.push_back(pt);
    }

    return result;
}