# Experiment questionnaire (fill in — leave blank if unknown)

This is **your** experiment, not the course toys and not the papers’ Pyrex / PS–PMMA / Cu examples. Put files in `data/experimental/` and point to them here.

## Sample and morphology

- [ ] Material(s) and layer stack (air / film / substrate, or something else):
- [ ] What should the model treat the surface as? (tick one, or explain)
  - [ ] continuous roughness (self-affine: σ, h, ξ)
  - [ ] islands or pits (coverage φ, height/depth Δ, size, spacing)
  - [ ] both
  - [ ] unknown — I need help deciding from the data
- [ ] Buried interfaces? Conformal roughness expected? (yes / no / unknown)

## Beam and instrument

- [ ] Probe: X-ray or neutron
- [ ] Wavelength λ or energy:
- [ ] Geometry: reflectivity / grazing-incidence / SAXS / other:
- [ ] Typical α, β or 2θ range:
- [ ] Measured scans available: specular / longitudinal diffuse / rocking (q∥) / full maps
- [ ] Approximate q-resolution and surface coherence length (if known):
- [ ] Polarization / beam size / slit settings (if known):

## Optical constants and contrast

- [ ] Refractive index n = 1 − δ + iβ, or SLD / electron density of each layer:
- [ ] Critical angle θ_c (measured or calculated):
- [ ] USER: if unknown, we can estimate from composition — tell us the composition.

## What “success” means

- [ ] Which features must a simulation reproduce? (Yoneda, Kiessig period, island side peaks, Porod slope, …)
- [ ] Which paper-style model is the starting point? (PRB continuous / Physica islands / both / unsure)
- [ ] File names of measurements you will add:

When this is filled, models belong in `src/xray_scattering/` and outputs in `data/simulated/`.
