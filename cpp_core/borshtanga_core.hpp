#pragma once

#include <complex>
#include <vector>

using Complex = std::complex<double>;

struct BorshtangaParams {
    double G;
    double rho;
    double Jp;
    double Jr;
    double L;
    double delta1;
};

// Точка кривой D-разбиения с информацией для штриховки
struct DCurvePoint {
    double re;          // Re(δ̂)
    double im;          // Im(δ̂)
    double hatch_dx;    // смещение конца штриха по X
    double hatch_dy;    // смещение конца штриха по Y
    double omega;       // частота, при которой посчитана точка (для отладки)
};

Complex computeDeltaHat(const BorshtangaParams& params, double omega);


std::vector<std::pair<double, double>> buildDCurve(
    const BorshtangaParams& params,
    double omegaMin, double omegaMax, int numPoints
);


std::vector<DCurvePoint> buildDCurveWithHatching(
    const BorshtangaParams& params,
    double omegaMin, double omegaMax, int numPoints,
    double hatch_length, int hatch_step
);