"""Regular expression patterns."""

from enum import Enum, IntEnum
from typing import Final

CN_CHAR: Final[str] = r'[\u4E00-\u9FA5]'


class LANGUAGE(Enum):
    EN = 'en'
    CN = 'cn'


class DomainNameMaxLen(IntEnum):
    """Max length of domain names."""

    EN = 67
    CN = 26


DOMAIN_NAMES: Final[dict[LANGUAGE, tuple[str, int]]] = {
    # 英文域名
    LANGUAGE.EN: (
        r'([a-zA-Z0-9]+)([a-zA-Z0-9-]*[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}',
        DomainNameMaxLen.EN,
    ),
    # 中文域名
    LANGUAGE.CN: (
        (
            r'('
            r'[\u4E00-\u9FA5]+([\u4E00-\u9FA5-]*[\u4E00-\u9FA5]+)*'
            r'|'
            r'('
            r'[a-zA-Z0-9\u4E00-\u9FA5]*[\u4E00-\u9FA5]+'
            r'([a-zA-Z0-9\u4E00-\u9FA5-]*[a-zA-Z0-9\u4E00-\u9FA5]+)*'
            r'|'
            r'[a-zA-Z0-9\u4E00-\u9FA5]+'
            r'([a-zA-Z0-9\u4E00-\u9FA5-]*[a-zA-Z0-9\u4E00-\u9FA5]*)*[\u4E00-\u9FA5]+'
            r'[a-zA-Z0-9\u4E00-\u9FA5-]*[a-zA-Z0-9\u4E00-\u9FA5]+'
            r')'
            r')'
            r'\.'
            r'([\u4E00-\u9FA5]{2,}|[a-zA-Z]{2,})'
        ),
        DomainNameMaxLen.CN,
    ),
}
