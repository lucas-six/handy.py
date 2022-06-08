import re
import string
from collections.abc import Iterator
from typing import Literal, Union

from .re_pattern import (
    CN_CHAR,
    DOMAIN_NAMES,
    EMAIL,
    FLOAT_NUMBER,
    HTML,
    ID_CN,
    LANGUAGE,
    LICENSE_PLATES,
    PHONE_CN,
    QQ_ID,
    RGB_HEX,
    WX_ID,
    IPv4,
)


def find_chinese_characters(
    s: str, iterred: bool = True
) -> Union[Iterator[re.Match[str]], list[str]]:
    """Find Chinese characters."""
    p = re.compile(CN_CHAR)
    return p.finditer(s) if iterred else p.findall(s)


def validate_float_number(s: str) -> bool:
    """Float number validator."""
    return _validate_by_regex(s, FLOAT_NUMBER)


def validate_ipv4(s: str) -> bool:
    """IPv4 addresses validator."""
    return _validate_by_regex(s, IPv4)


def validate_email(s: str) -> bool:
    """Email address validator."""
    return _validate_by_regex(s, EMAIL, re.IGNORECASE)


def validate_html(s: str) -> bool:
    """HTML elements or tags validator."""
    return _validate_by_regex(s, HTML, re.IGNORECASE | re.DOTALL)


def validate_domain_name(s: str, language: LANGUAGE = LANGUAGE.EN) -> bool:
    """Domain name validator."""
    dn = DOMAIN_NAMES[language]
    m = re.match(r'(' + dn[0] + r')$', s, re.IGNORECASE)
    if m:
        return len(s) <= dn[1]
    return False


def validate_rgb_hex(s: str) -> bool:
    """Color RGB hex validator."""
    return _validate_by_regex(s, RGB_HEX, re.IGNORECASE)


def validate_password_strength(s: str, min_len: int) -> bool:
    """Password strength validator.

    包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符
    """
    if min_len < 2:
        raise ValueError('minimal length of password must greater than 1')
    m = re.match(
        r'.*(?=.{'
        + str(min_len)
        + r',})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$',
        s,
    )
    return m is not None


def validate_license_plate(s: str, region: Literal['cn', 'hk']) -> bool:
    """License plate validator."""
    return _validate_by_regex(s, LICENSE_PLATES[region])


def validate_wx_id(s: str) -> bool:
    """Wechat(Wexin) ID validator."""
    return _validate_by_regex(s, WX_ID)


def validate_qq_id(s: str) -> bool:
    """QQ ID validator."""
    return _validate_by_regex(s, QQ_ID)


def validate_phone_cn(s: str) -> bool:
    """Chinese phone number validator."""
    return _validate_by_regex(s, PHONE_CN)


def validate_id_cn(s: str) -> bool:
    """Chinese ID validator."""
    return _validate_by_regex(s, ID_CN)


def ispunctuation(s: str) -> bool:
    """Return `True` if all characters in `s` are ASCII punctuation characters
    in the C locale."""
    if not s:
        return False
    for c in s:
        if c not in string.punctuation:
            return False
    return True


def _validate_by_regex(s: str, pattern: str, flags: int = 0) -> bool:
    """Validator by Regex."""
    m = re.match(r'(' + pattern + r')$', s, flags=flags)
    return m is not None
