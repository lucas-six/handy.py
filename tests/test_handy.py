import re
import string

import pytest

from src.handy import find_chinese_characters, ispunctuation


class TestHandy:
    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            (string.printable, []),
            ('纯中文', ['纯', '中', '文']),
            (f'中{string.printable}文', ['中', '文']),
        ),
    )
    def test_find_chinese_characters(self, s: str, expected: list[str]):
        assert expected == find_chinese_characters(s, iterred=False)

        for m, e in zip(find_chinese_characters(s), expected):
            assert isinstance(m, re.Match)
            assert m.group() == e

    def test_ispunctuation(self):
        assert not ispunctuation('')

        for c in string.printable:
            if c in string.punctuation:
                assert ispunctuation(c)
            else:
                assert not ispunctuation(c)
