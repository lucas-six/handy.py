import random
import re
import string

import pytest

from src.handy import (
    find_chinese_characters,
    ispunctuation,
    re_pattern,
    validate_domain_name_en,
)


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

    @pytest.fixture
    def loop_times(self) -> int:
        return 1000

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc', False),
            ('123', False),
            ('!@#', False),
            ('abc123', False),
            ('abc!@#', False),
            ('123!@#', False),
            ('abc123!@#', False),
        ),
    )
    def test_validate_domain_name_en_without_dot(self, s: str, expected: bool):
        self._validate_domain_name_en(s, expected)

    def test_validate_domain_name_en_without_dot_loop(self, loop_times: int):
        while loop_times:
            s = self._gen_domain_name_en_without_dot(loop_times)
            self._validate_domain_name_en(s, False)
            loop_times -= 1

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc.', False),
            ('123.', False),
            ('!@#.', False),
            ('abc123.', False),
            ('abc!@#.', False),
            ('123!@#.', False),
            ('abc123!@#.', False),
            ('abc..', False),
            ('123..', False),
            ('!@#..', False),
            ('abc123..', False),
            ('abc!@#..', False),
            ('123!@#..', False),
            ('abc123!@#..', False),
        ),
    )
    def test_validate_domain_name_en_ends_with_dot(self, s: str, expected: bool):
        self._validate_domain_name_en(s, expected)

    def test_validate_domain_name_en_ends_ends_with_dot_loop(self, loop_times: int):
        while loop_times:
            s = self._gen_domain_name_en_ends_with_dot(loop_times)
            self._validate_domain_name_en(s, False)
            loop_times -= 1

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc.d', False),
            ('123.d', False),
            ('abc123.d', False),
            ('abc.dd', True),
            ('123.dd', True),
            ('abc123.dd', True),
            ('abc.ddd', True),
            ('123.ddd', True),
            ('abc123.ddd', True),
            ('a.ddd', True),
        ),
    )
    def test_validate_domain_name_en_ends_with_one(self, s: str, expected: bool):
        self._validate_domain_name_en(s, expected)

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('a.1', False),
            ('a.12', False),
            ('a.123', False),
            ('a.1a', False),
            ('a.a1', False),
            ('a.a1b', False),
            ('a.ab', True),
        ),
    )
    def test_validate_domain_name_en_ends_with_digits(self, s: str, expected: bool):
        self._validate_domain_name_en(s, expected)

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('-abc.org', False),
            ('abc-.org', False),
            ('a-bc.org', True),
            ('a-b-c.org', True),
            ('a-b-c.-org', False),
            ('a-b-c.o-rg', False),
            ('a-b-c.org-', False),
        ),
    )
    def test_validate_domain_name_en_contains_dots(self, s: str, expected: bool):
        self._validate_domain_name_en(s, expected)

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc.org', True),
            (
                # ''.join(random.choices(
                #   string.ascii_letters + string.digits,
                #   k=re_pattern.DOMAIN_NAME_EN_MAX_LEN - len('.org)
                'HEXk36kBEBOX0FlilNJZkR9B08VnoBgdNcnazAd6UYgKz0MSJkWrZivhU1rkZYf.org',
                True,
            ),
            (
                # ''.join(random.choices(
                #   string.ascii_letters + string.digits,
                #   k=re_pattern.DOMAIN_NAME_EN_MAX_LEN - len('.org) + 1
                'HEXk36kBEBOX0FlilNJZkR9B08VnoBgdNcnazAd6UYgKz0MSJkWrZivhU1rkZYfg.org',
                False,
            ),
        ),
    )
    def test_validate_domain_en_len(self, s: str, expected: bool):
        self._validate_domain_name_en(s, expected)

    def test_ispunctuation(self):
        assert not ispunctuation('')

        for c in string.printable:
            if c in string.punctuation:
                assert ispunctuation(c)
            else:
                assert not ispunctuation(c)

    def _gen_domain_name_en_without_dot(self, seed: int) -> str:
        """Generate English domain name without dot."""
        random.seed(seed)
        return ''.join(
            random.choices(
                string.printable.replace('.', ''),
                k=random.randint(1, re_pattern.DOMAIN_NAME_EN_MAX_LEN),
            )
        )

    def _gen_domain_name_en_ends_with_dot(self, seed: int) -> str:
        """Generate English domain name ending with dot(s)."""
        random.seed(seed)
        return ''.join(
            random.choices(
                string.printable.replace('.', ''),
                k=random.randint(1, (re_pattern.DOMAIN_NAME_EN_MAX_LEN - 1) // 2),
            )
        ) + '.' * random.randint(1, (re_pattern.DOMAIN_NAME_EN_MAX_LEN - 1) // 2)

    def _validate_domain_name_en(self, s: str, expected: bool):
        result = validate_domain_name_en(s)
        if expected:
            assert result
        else:
            # not match
            assert not result
