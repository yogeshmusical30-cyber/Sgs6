"""Small compatibility helpers for Raspberry Pi deployments."""
from __future__ import annotations

import importlib
import sys
from typing import Any


def optional_import(module_name: str) -> Any:
    """Return an imported module or None when the dependency is missing."""
    try:
        return importlib.import_module(module_name)
    except Exception:
        return None


def running_as_script() -> bool:
    return __package__ in (None, "") or sys.path[0].endswith("SGS")
