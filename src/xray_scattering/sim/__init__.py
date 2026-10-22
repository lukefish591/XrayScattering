"""Illustrative surface-scattering simulation (Born / DWBA toys).

Not experimental data. Intensities omit overall (Nb)², area, and flux.
"""

from xray_scattering.sim.analysis import (
    empirical_correlation,
    fit_line_from_measurement,
    fit_self_affine,
    invert_C_from_sdiff,
    radial_psd_from_C,
    rebuild_from_C,
)
from xray_scattering.sim.correlations import (
    C_capillary,
    C_gaussian,
    C_self_affine,
    correlation_function,
)
from xray_scattering.sim.forward import (
    born_s_diff,
    born_s_diff_qz,
    fresnel_rt,
    simulate_measurement,
    specular_dw,
)
from xray_scattering.sim.hankel import hankel0, inverse_hankel0
from xray_scattering.sim.params import MeasureParams, SurfaceParams
from xray_scattering.sim.surface import Surface, generate_surface
from xray_scattering.sim.sweep import (
    DiagnosticReport,
    plot_report,
    run_diagnostic_sweep,
    score_locked_surface,
)

__all__ = [
    "C_capillary",
    "C_gaussian",
    "C_self_affine",
    "MeasureParams",
    "Surface",
    "SurfaceParams",
    "born_s_diff",
    "born_s_diff_qz",
    "correlation_function",
    "empirical_correlation",
    "DiagnosticReport",
    "fit_line_from_measurement",
    "fit_self_affine",
    "fresnel_rt",
    "generate_surface",
    "hankel0",
    "inverse_hankel0",
    "invert_C_from_sdiff",
    "plot_report",
    "radial_psd_from_C",
    "rebuild_from_C",
    "run_diagnostic_sweep",
    "score_locked_surface",
    "simulate_measurement",
    "specular_dw",
]
