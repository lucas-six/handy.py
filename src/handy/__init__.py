"""Collection of handy utils for Python."""

from ._handy import (
    find_chinese_characters,
    ispunctuation,
    validate_domain_name,
    validate_license_plate,
)

__version__ = '0.0.1-alpha.3'

__all__ = [
    'find_chinese_characters',
    'validate_domain_name',
    'validate_license_plate',
    'ispunctuation',
]
