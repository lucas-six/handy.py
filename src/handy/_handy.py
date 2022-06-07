import re
import string
from collections.abc import Iterator
from typing import Union

from .re_pattern import CN_CHAR, DOMAIN_NAMES, LANGUAGE


def find_chinese_characters(
    s: str, iterred: bool = True
) -> Union[Iterator[re.Match[str]], list[str]]:
    """Find Chinese characters."""
    p = re.compile(CN_CHAR)
    return p.finditer(s) if iterred else p.findall(s)


def validate_domain_name(s: str, language: LANGUAGE = LANGUAGE.EN) -> bool:
    """Domain name validator."""
    dn = DOMAIN_NAMES[language]
    p = re.compile(dn[0] + r'$', re.IGNORECASE)
    m = p.match(s)
    if m:
        return len(s) <= dn[1]
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
