from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class SurfaceParams:
    """Illustrative surface knobs. Lengths in Å."""

    family: str = "self-affine"  # self-affine | gaussian | capillary
    sigma: float = 5.0
    xi: float = 40.0
    h: float = 0.5
    B: float = 8.0
    xi_ir: float = 80.0
    a_uv: float = 1.0
    N: int = 96
    L: float = 384.0
    seed: int = 1
    islands: bool = False
    phi: float = 0.25
    delta: float = 12.0
    island_R: float = 36.0
    island_d: float = 100.0

    def cache_key(self) -> tuple:
        return (
            self.family,
            self.sigma,
            self.xi,
            self.h,
            self.B,
            self.xi_ir,
            self.a_uv,
            self.N,
            self.L,
            self.seed,
            self.islands,
            self.phi,
            self.delta,
            self.island_R,
            self.island_d,
        )


@dataclass(frozen=True)
class MeasureParams:
    """Illustrative instrument knobs. Angles in degrees, lengths in Å."""

    wavelength: float = 1.54
    alpha_deg: float = 0.55
    scan: str = "rocking"  # specular | rocking | qmap
    n_pts: int = 81
    rock_range_deg: float = 0.45
    qz_min: float = 0.05
    qz_max: float = 0.22
    use_dwba: bool = False
    delta_n: float = 6.3e-6
    beta_n: float = 8.5e-8
    dq: float = 0.002
    xi_coh: float = 600.0
    footprint: bool = True
    noise: float = 0.0
    background: float = 0.0
    pixel_dq: float = 0.0
    counts_scale: float = 1.0e5
    seed: int = 0

    def cache_key(self) -> tuple:
        return tuple(asdict(self).values())


def params_to_json(surface: SurfaceParams, measure: MeasureParams) -> dict:
    return {
        "illustrative": True,
        "not_experimental_data": True,
        "surface": asdict(surface),
        "measure": asdict(measure),
    }
