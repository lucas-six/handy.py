import random
import re
import string

import pytest

from src.handy import (
    find_chinese_characters,
    ispunctuation,
    re_pattern,
    validate_domain_name,
    validate_license_plate,
    validate_qq_id,
    validate_wx_id,
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
    def domain_name_max_len_en(self):
        return re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.EN][1]

    @pytest.fixture
    def domain_name_max_len_cn(self):
        return re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.CN][1]

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
        self._validate_domain_name(s, expected)

    def test_validate_domain_name_en_without_dot_loop(
        self, loop_times: int, domain_name_max_len_en: int
    ):
        while loop_times:
            s = self._gen_domain_name_en_without_dot(loop_times, domain_name_max_len_en)
            self._validate_domain_name(s, False)
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
        self._validate_domain_name(s, expected)

    def test_validate_domain_name_en_ends_ends_with_dot_loop(
        self, loop_times: int, domain_name_max_len_en: int
    ):
        while loop_times:
            s = self._gen_domain_name_en_ends_with_dot(
                loop_times, domain_name_max_len_en
            )
            self._validate_domain_name(s, False)
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
        self._validate_domain_name(s, expected)

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
        self._validate_domain_name(s, expected)

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
        self._validate_domain_name(s, expected)

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
        self._validate_domain_name(s, expected)

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('纯中文', False),
            ('abc', False),
            ('123', False),
            ('abc中文', False),
            ('123中文', False),
            ('纯中文.', False),
            ('abc.', False),
            ('123.', False),
            ('中文abc.', False),
            ('中文123.', False),
            ('纯中文..', False),
            ('abc..', False),
            ('123..', False),
            ('中文abc..', False),
            ('中文123..', False),
            ('纯中文.d', False),
            ('abc.d', False),
            ('123.d', False),
            ('中文abc.d', False),
            ('中文123.d', False),
            ('纯中文.dd', True),
            ('abc.dd', False),
            ('123.dd', False),
            ('中文abc.dd', True),
            ('中文123.ddd', True),
            ('纯中文.ab', True),
            ('纯中文.中文', True),
            ('中文abc.ab', True),
            ('中文abc.中文', True),
            ('中文abc.a中文', False),
            ('纯中文.a中文', False),
            ('abc.a中文', False),
            ('-中文.org', False),
            ('中文-.org', False),
            ('a-中文.org', True),
            ('a-中文-c.org', True),
            ('a-中文-c.-org', False),
            ('a-中文-c.o-rg', False),
            ('a-中文-c.org-', False),
            ('-中文.中文', False),
            ('中文-.中文', False),
            ('a-中文.中文', True),
            ('a-中文-c.中文', True),
            ('a-中文-c.-中文', False),
            ('a-中文-c.中-文', False),
            ('a-中文-c.中文-', False),
            (
                chr(random.randint(ord('\u4E00'), ord('\u9FA5') + 1))
                * (re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.CN][1] - len('.org'))
                + '.org',
                True,
            ),
            (
                chr(random.randint(ord('\u4E00'), ord('\u9FA5') + 1))
                * (re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.CN][1] - len('.org') + 1)
                + '.org',
                False,
            ),
        ),
    )
    def test_validate_domain_cn(self, s: str, expected: bool):
        self._validate_domain_name(s, expected, re_pattern.LANGUAGE.CN)

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('湘A12345', True),
            ('AA12345', False),
            ('中A12345', False),
            ('湘A1234D', True),
            ('湘A1234DF', True),
            ('湘A1234', False),
            ('湘a12345', False),
            ('湘A1234d', False),
            ('湘A12345678', False),
            ('湘A123.5', False),
        ),
    )
    def test_validate_license_plate_cn(self, s: str, expected: bool):
        result = validate_license_plate(s, 'cn')
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('a' * 6, True),
            ('A' * 6, True),
            ('Aa' * 3, True),
            ('1' * 6, False),
            ('a123' * 2, True),
            ('1abcde', False),
            ('a_123' * 2, True),
            ('a-123' * 2, True),
            ('a' * 20, True),
            ('a' * 21, False),
            (
                random.choice(string.ascii_letters)
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits + '-_',
                        k=random.randint(6 - 1, 20 - 1),
                    )
                ),
                True,
            ),
        ),
    )
    def test_validate_wx_id(self, s: str, expected: bool):
        result = validate_wx_id(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('a' * 5, False),
            ('A' * 5, False),
            ('Aa' * 3, False),
            ('1' * 5, True),
            ('a1234', False),
            ('1abcd', False),
            ('a_1234', False),
            ('a-1234', False),
            ('1' * 5, True),
            ('1' * 12, False),
            (
                str(random.randint(1, 9))
                + ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(5 - 1, 11 - 1),
                    )
                ),
                True,
            ),
        ),
    )
    def test_validate_qq_id(self, s: str, expected: bool):
        result = validate_qq_id(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    def test_ispunctuation(self):
        assert not ispunctuation('')

        for c in string.printable:
            if c in string.punctuation:
                assert ispunctuation(c)
            else:
                assert not ispunctuation(c)

    def _gen_domain_name_en_without_dot(self, seed: int, max_len: int) -> str:
        """Generate English domain name without dot."""
        random.seed(seed)
        return ''.join(
            random.choices(
                string.printable.replace('.', ''),
                k=random.randint(1, max_len),
            )
        )

    def _gen_domain_name_en_ends_with_dot(self, seed: int, max_len: int) -> str:
        """Generate English domain name ending with dot(s)."""
        random.seed(seed)
        return ''.join(
            random.choices(
                string.printable.replace('.', ''),
                k=random.randint(1, (max_len - 1) // 2),
            )
        ) + '.' * random.randint(1, (max_len - 1) // 2)

    def _validate_domain_name(
        self,
        s: str,
        expected: bool,
        language: re_pattern.LANGUAGE = re_pattern.LANGUAGE.EN,
    ):
        result = validate_domain_name(s, language)
        if expected:
            assert result
        else:
            # not match
            assert not result
