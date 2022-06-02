import re
import string

import pytest

from src.handy import re_pattern


class TestRePattern:
    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            (string.printable, []),
            ('纯中文', ['纯', '中', '文']),
            (f'中{string.printable}文', ['中', '文']),
        ),
    )
    def test_chinese_character(
        self,
        s: str,
        expected: list[str],
    ):
        p = re.compile(re_pattern.CN_CHAR)
        assert p.findall(s) == expected
