"""Regular expression patterns."""

from typing import Final

CN_CHAR: Final[str] = r'[\u4E00-\u9FA5]'

DOMAIN_EN_MAX_LEN: Final[int] = 67
DOMAIN_EN: Final[str] = r'[a-zA-Z0-9]+[a-zA-Z0-9-]*[a-zA-Z0-9]+\.[a-zA-Z]{2,}'  # 英文域名
DOMAIN_CN: Final[str] = (
    r'('
    r'[a-zA-Z0-9]'
    r'|'
    f'{CN_CHAR}'
    r')+'
    r'[-]*'
    r'('
    r'[a-zA-Z0-9]'
    r'|'
    f'{CN_CHAR}'
    r')+'
    r'\.'
    r'('
    r'[a-zA-Z]{2,}'
    r'|'
    f'{CN_CHAR}'
    r'{2,})'
)  # 中文域名
