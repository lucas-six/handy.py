"""Regular expression patterns."""

from enum import Enum, IntEnum
from typing import Final, Literal

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
            r'([\u4E00-\u9FA5]{2,}|[a-zA-Z]{2,})'  # 根域名
        ),
        DomainNameMaxLen.CN,
    ),
}

# 车牌号
LICENSE_PLATES: Final[dict[Literal['cn', 'hk'], str]] = {
    'cn': (
        r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z]'
        r'[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}'
        r'|'
        r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z]'
        r'[A-Z0-9]{6}$'  # 新能源
    ),
    'hk': r'[A-Z]{2}[0-9]{3,4}',  # 香港
}

# 微信号正则表达式，6至20位，以字母开头，字母，数字，减号，下划线
WX_ID: Final[str] = r'[a-zA-Z][a-zA-Z0-9_-]{5,19}'

# QQ号正则表达式，5至11位数字
QQ_ID: Final[str] = r'[1-9][0-9]{4,10}'
