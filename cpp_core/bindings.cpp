#include <pybind11/pybind11.h>
#include <pybind11/stl.h>      
#include <pybind11/complex.h>  
#include "borshtanga_core.hpp"

namespace py = pybind11;

PYBIND11_MODULE(borshtanga_core, m) {
    m.doc() = "C++ ядро для расчёта устойчивости расточной борштанги";

    
    py::class_<BorshtangaParams>(m, "BorshtangaParams")
        .def(py::init<>())  
        .def_readwrite("G", &BorshtangaParams::G)
        .def_readwrite("rho", &BorshtangaParams::rho)
        .def_readwrite("Jp", &BorshtangaParams::Jp)
        .def_readwrite("Jr", &BorshtangaParams::Jr)
        .def_readwrite("L", &BorshtangaParams::L)
        .def_readwrite("delta1", &BorshtangaParams::delta1);

    // Регистрируем функции
    m.def("compute_delta_hat", &computeDeltaHat,
          "Вычислить значение δ̂ для заданной частоты ω",
          py::arg("params"), py::arg("omega"));

    m.def("build_d_curve", &buildDCurve,
          "Построить кривую D-разбиения для заданного диапазона частот",
          py::arg("params"),
          py::arg("omega_min"),
          py::arg("omega_max"),
          py::arg("num_points"));
}