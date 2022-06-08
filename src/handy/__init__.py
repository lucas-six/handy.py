"""Collection of handy utils for Python."""

from ._handy import (
    find_chinese_characters,
    ispunctuation,
    validate_domain_name,
    validate_email,
    validate_float_number,
    validate_id_cn,
    validate_license_plate,
    validate_password_strength,
    validate_phone_cn,
    validate_qq_id,
    validate_rgb_hex,
    validate_wx_id,
)

__version__ = '0.0.1-alpha.7'

__all__ = [
    'find_chinese_characters',
    'validate_float_number',
    'validate_email',
    'validate_domain_name',
    'validate_rgb_hex',
    'validate_password_strength',
    'validate_license_plate',
    'validate_wx_id',
    'validate_qq_id',
    'validate_phone_cn',
    'validate_id_cn',
    'ispunctuation',
]
