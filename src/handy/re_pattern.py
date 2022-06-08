"""Regular expression patterns."""

from enum import Enum, IntEnum
from typing import Final, Literal

# 浮点数
FLOAT_NUMBER: Final[str] = r'-?\d+(\.\d+)?'

# IPv4
IPv4: Final[
    str
] = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'

# 中文字符
CN_CHAR: Final[str] = r'[\u4E00-\u9FA5]'

# Email address
EMAIL: Final[str] = r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*'

# HTML标记的正则表达式
HTML: Final[str] = r'<\S+[^>]*>.*?|<.*? />'


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

# 颜色 RGB 十六进制正则表达式
RGB_HEX: Final[str] = r'#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})'

# 车牌号
LICENSE_PLATES: Final[dict[Literal['cn', 'hk'], str]] = {
    'cn': (
        r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z]'
        r'[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}'
        r'|'
        r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z]'
        r'[A-Z0-9]{6}$'  # 新能源
    ),
    'hk': r'[A-Z]{2}\d{3,4}',  # 香港
}

# 微信号正则表达式，6至20位，以字母开头，字母，数字，减号，下划线
WX_ID: Final[str] = r'[a-zA-Z][a-zA-Z0-9_-]{5,19}'

# QQ号正则表达式，5至11位数字
QQ_ID: Final[str] = r'[1-9]\d{4,10}'

# 中国手机号码正则表达式
PHONE_CN: Final[
    str
] = r'(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}'

# 中国身份证号码正则表达式，15-18位数字，最后一位是校验位，可能为数字或字符X
ID_CN: Final[str] = r'\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)'
