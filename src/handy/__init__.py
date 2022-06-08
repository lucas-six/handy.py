"""Collection of handy utils for Python."""

from ._handy import (
    find_chinese_characters,
    ispunctuation,
    validate_domain_name,
    validate_license_plate,
    validate_qq_id,
    validate_rgb_hex,
    validate_wx_id,
)

__version__ = '0.0.1-alpha.6'

__all__ = [
    'find_chinese_characters',
    'validate_domain_name',
    'validate_rgb_hex',
    'validate_license_plate',
    'validate_wx_id',
    'validate_qq_id',
    'ispunctuation',
]
