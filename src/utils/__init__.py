"""Utility functions for the EcoLogical-Extractor package."""

from .external_deps import (
    EXTERNAL_DEPENDENCIES,
    check_all_dependencies,
    check_dependency,
    get_env_var_instructions,
    get_platform,
)

__all__ = [
    "check_dependency",
    "check_all_dependencies",
    "get_platform",
    "get_env_var_instructions",
    "EXTERNAL_DEPENDENCIES",
]
