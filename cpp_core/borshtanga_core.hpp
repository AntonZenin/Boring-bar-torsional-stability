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


Complex computeDeltaHat(const BorshtangaParams& params, double omega);

std::vector<std::pair<double, double>> buildDCurve(
    const BorshtangaParams& params,
    double omegaMin,
    double omegaMax,
    int numPoints
);