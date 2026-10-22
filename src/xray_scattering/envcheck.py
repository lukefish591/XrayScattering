"""Print installed versions of the scientific stack used for this project."""

from __future__ import annotations

import importlib
import sys

PACKAGES = ("numpy", "scipy", "matplotlib", "pandas", "h5py")


def collect_versions() -> dict[str, str]:
    versions: dict[str, str] = {"python": sys.version.split()[0]}
    for name in PACKAGES:
        module = importlib.import_module(name)
        versions[name] = getattr(module, "__version__", "unknown")
    return versions


def main() -> None:
    print("XrayScattering environment")
    for name, version in collect_versions().items():
        print(f"  {name}: {version}")


if __name__ == "__main__":
    main()
