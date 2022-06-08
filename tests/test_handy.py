import random
import re
import string

import pytest

from src.handy import (
    find_chinese_characters,
    ispunctuation,
    re_pattern,
    validate_domain_name,
    validate_email,
    validate_float_number,
    validate_html,
    validate_id_cn,
    validate_ipv4,
    validate_license_plate,
    validate_password_strength,
    validate_phone_cn,
    validate_qq_id,
    validate_rgb_hex,
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

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('12', True),
            ('12.', False),
            ('12.1', True),
            ('-12.1', True),
            ('-12', True),
            ('0', True),
            ('0.0', True),
        ),
    )
    def test_validate_float_number(self, s: str, expected: bool):
        result = validate_float_number(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('192.1.1.1', True),
            ('192.', False),
            ('192.1', False),
            ('192.1.1', False),
            ('192.1.1.1.1', False),
            ('192..1.1.1', False),
            ('192.1.1.1.', False),
            ('.192.1.1.1', False),
        ),
    )
    def test_validate_ipv4(self, s: str, expected: bool):
        result = validate_ipv4(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc', False),
            ('ABC', False),
            ('aBc', False),
            ('<br>', True),
            ('<a>a</a>', True),
            ('<A>a</A>', True),
            ('<img/>', True),
            ('<img />', True),
            ('<a href="xxx">aaa</a>', True),
            ('<a \teditable>aaa</a>', True),
            ('<section>aaa</section>', True),
            ('<sEction>aaa</sectIon>', True),
            ('< section>aaa</section>', False),
            ('<section><section>aaa</section></section>', True),
            ('<section> <section>a a a</section> </section>', True),
            ('<section> \t<section>a a \ta\t</section> \t</section>', True),
            ('<section>\n<section>aaa </section>\n\n</section>', True),
            ('<section>\n<section>aa\ta </section>\n\n</section>', True),
        ),
    )
    def test_validate_html(self, s: str, expected: bool):
        result = validate_html(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('abc', False),
            ('ABC', False),
            ('aBc', False),
            ('123', False),
            ('abc123', False),
            ('ABC123', False),
            ('aBc123', False),
            ('123abc', False),
            ('abc@', False),
            ('ABC@', False),
            ('aBc@', False),
            ('123@', False),
            ('abc123@', False),
            ('aBc123@', False),
            ('123abc@', False),
            ('abc@a', False),
            ('ABC@a', False),
            ('aBc@a', False),
            ('123@a', False),
            ('abc123@a', False),
            ('aBc123@a', False),
            ('123abc@a', False),
            ('abc@a.b', True),
            ('ABC@a.b', True),
            ('aBc@a.b', True),
            ('123@a.b', True),
            ('abc123@a.b', True),
            ('aBc123@a.b', True),
            ('123abc@a.b', True),
            ('ab.@a.b', False),
            ('ab-c@a.b', True),
            ('ab_c@a.b', True),
            ('ab.c@a.b', True),
            ('ab+c@a.b', True),
            ('abc@a-b.c', True),
            ('abc@a.b.c', True),
        ),
    )
    def test_validate_email(self, s: str, expected: bool):
        result = validate_email(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

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
            ('#123', True),
            ('#123456', True),
            ('#1234567', False),
            ('123', False),
            ('123456', False),
            ('#abc', True),
            ('#abcdef', True),
            ('#12345', False),
            ('#fffff', False),
            ('#FFFFF', False),
            ('#ABC', True),
            ('#FFFFFF', True),
            ('#GGG', False),
            ('#GGGGGG', False),
        ),
    )
    def test_validate_rgb_hex(self, s: str, expected: bool):
        result = validate_rgb_hex(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'min_len', 'expected'),
        (
            ('Aa1!56', 6, True),
            ('Aa1!56', 1, False),  # minimal length not enough
            ('Aa1!5', 6, False),  # length not enough
            ('Aa1!567', 6, True),
            ('Aa1456', 6, False),  # special characters required
            ('123456', 6, False),  # pure digits
            ('A12!45', 6, False),  # lowercase letter required
            ('a12!45', 6, False),  # uppercase letter required
            ('abcdef', 6, False),  # pure lowercase letters
            ('ABCDEF', 6, False),  # pure uppercase letters
            ('AbCdEf', 6, False),  # digits and special characters required
        ),
    )
    def test_validate_password_strength(self, s: str, min_len: int, expected: bool):
        if min_len < 2:
            with pytest.raises(ValueError):
                validate_password_strength(s, min_len)
            return

        result = validate_password_strength(s, min_len)
        if expected:
            assert result
        else:
            # not match
            assert not result

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

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('13800000000', True),
            ('13900000000', True),
            ('13600000000', True),
            ('13500000000', True),
            ('13400000000', True),
            ('18600000000', True),
            ('18500000000', True),
            ('18900000000', True),
            ('17500000000', True),
            ('17700000000', True),
            ('138000000000', False),
            ('11100000000', False),
        ),
    )
    def test_validate_phone_cn(self, s: str, expected: bool):
        result = validate_phone_cn(s)
        if expected:
            assert result
        else:
            # not match
            assert not result

    @pytest.mark.parametrize(
        ('s', 'expected'),
        (
            ('430000000000000000', True),
            ('43000000000000000X', True),
            ('4300000000000000000', False),
            ('123456789011111', True),
            ('12345678901111X', False),
            ('43000000000000000', False),
        ),
    )
    def test_validate_id_cn(self, s: str, expected: bool):
        result = validate_id_cn(s)
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
