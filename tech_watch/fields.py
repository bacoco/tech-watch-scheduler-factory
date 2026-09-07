"""Small shared profile field checks, without imports from the profile validator."""
from .common import require


def text(value, name):
    require(isinstance(value, str) and 1 <= len(value.strip()) <= 2000,
            f"{name}: nonempty text (max 2000 characters) required")
    require(not any(ord(c) < 32 for c in value), f"{name}: use single-line text")


def texts(value, name, nonempty=False):
    require(isinstance(value, list), f"{name}: list required")
    require(not nonempty or bool(value), f"{name}: cannot be empty")
    require(len(value) <= 30, f"{name}: split scope before exceeding 30 entries")
    for item in value:
        text(item, name)
