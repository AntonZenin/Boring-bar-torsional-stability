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

    py::class_<DCurvePoint>(m, "DCurvePoint")
        .def_readonly("re", &DCurvePoint::re)
        .def_readonly("im", &DCurvePoint::im)
        .def_readonly("hatch_dx", &DCurvePoint::hatch_dx)
        .def_readonly("hatch_dy", &DCurvePoint::hatch_dy)
        .def_readonly("omega", &DCurvePoint::omega);

    m.def("compute_delta_hat", &computeDeltaHat,
          py::arg("params"), py::arg("omega"));

    m.def("build_d_curve", &buildDCurve,
          py::arg("params"), py::arg("omega_min"),
          py::arg("omega_max"), py::arg("num_points"));

    m.def("build_d_curve_with_hatching", &buildDCurveWithHatching,
          py::arg("params"),
          py::arg("omega_min"),
          py::arg("omega_max"),
          py::arg("num_points"),
          py::arg("hatch_length"),
          py::arg("hatch_step"));
}