import re
import string
from collections.abc import Iterator
from typing import Union

from .re_pattern import CN_CHAR, DOMAIN_NAME_EN, DOMAIN_NAME_EN_MAX_LEN


def find_chinese_characters(
    s: str, iterred: bool = True
) -> Union[Iterator[re.Match[str]], list[str]]:
    """Find Chinese characters."""
    p = re.compile(CN_CHAR)
    return p.finditer(s) if iterred else p.findall(s)


def is_domain_name_en(s: str) -> bool:
    """Whether string `s` is english domain name."""
    p = re.compile(DOMAIN_NAME_EN + r'$', re.IGNORECASE)
    m = p.match(s)
    if m:
        return len(s) <= DOMAIN_NAME_EN_MAX_LEN
    return False


def ispunctuation(s: str) -> bool:
    """Return `True` if all characters in `s` are ASCII punctuation characters
    in the C locale."""
    if not s:
        return False
    for c in s:
        if c not in string.punctuation:
            return False
    return True
