from xray_scattering.envcheck import collect_versions


def test_scientific_stack_imports():
    versions = collect_versions()
    assert versions["python"]
    for name in ("numpy", "scipy", "matplotlib", "pandas", "h5py"):
        assert versions[name] != "unknown"
