import random
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
        assert re.findall(re_pattern.CN_CHAR, s) == expected

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
    def test_float_number(
        self,
        s: str,
        expected: list[str],
    ):
        m = re.match(r'(' + re_pattern.FLOAT_NUMBER + r')$', s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_ipv4(
        self,
        s: str,
        expected: list[str],
    ):
        m = re.match(r'(' + re_pattern.IPv4 + r')$', s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_email(
        self,
        s: str,
        expected: list[str],
    ):
        m = re.match(r'(' + re_pattern.EMAIL + r')$', s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
            ('<sEction>aaa</section>', True),
            ('< section>aaa</section>', False),
            ('<section><section>aaa</section></section>', True),
            ('<section> <section>a a a</section> </section>', True),
            ('<section> \t<section>a a \ta\t</section> \t</section>', True),
            ('<section>\n<section>aaa </section>\n\n</section>', True),
            ('<section>\n<section>aa\ta </section>\n\n</section>', True),
        ),
    )
    def test_html(
        self,
        s: str,
        expected: list[str],
    ):
        m = re.match(r'(' + re_pattern.HTML + r')$', s, re.IGNORECASE | re.DOTALL)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
            ('a.1', False),
            ('a.12', False),
            ('a.123', False),
            ('a.1a', False),
            ('a.a1', False),
            ('a.a1b', False),
            ('a.ab', True),
            ('-abc.org', False),
            ('abc-.org', False),
            ('a-bc.org', True),
            ('a-b-c.org', True),
            ('a-b-c.-org', False),
            ('a-b-c.o-rg', False),
            ('a-b-c.org-', False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, 1024),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(string.ascii_letters, k=random.randint(2, 1024))
                ),
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, 1024),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits + '-',
                        k=random.randint(1, 1024),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, 1024),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(string.ascii_letters, k=random.randint(2, 1024))
                ),
                True,
            ),
        ),
    )
    def test_domain_name_en(self, s: str, expected: bool):
        m = re.match(
            r'(' + re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.EN][0] + r')$',
            s,
            re.IGNORECASE,
        )
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(string.ascii_letters, k=random.randint(2, 1024))
            #     ),
            #     True,
            # ),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             ), k=random.randint(2, 1024))
            #     ),
            #     True,
            # ),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits
            #             + '-',
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(string.ascii_letters, k=random.randint(2, 1024))
            #     ),
            #     True,
            # ),
            # (
            #     ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits
            #             + '-',
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             )
            #             + string.ascii_letters
            #             + string.digits,
            #             k=random.randint(1, 1024),
            #         )
            #     )
            #     + '.'
            #     + ''.join(
            #         random.choices(
            #             ''.join(
            #                 [chr(_i) \
            #                       for _i in range(ord('\u4E00'), ord('\u9FA5') + 1)]
            #             ),
            #             k=random.randint(2, 1024),
            #         )
            #     ),
            #     True,
            # ),
        ),
    )
    def test_domain_name_cn(self, s: str, expected: bool):
        p = re.compile(
            r'(' + re_pattern.DOMAIN_NAMES[re_pattern.LANGUAGE.CN][0] + r')$',
            re.IGNORECASE,
        )
        m = p.match(s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_rgb_hex(self, s: str, expected: bool):
        p = re.compile(r'(' + re_pattern.RGB_HEX + r')$')
        m = p.match(s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_license_plate(self, s: str, expected: bool):
        p = re.compile(r'(' + re_pattern.LICENSE_PLATES['cn'] + r')$')
        m = p.match(s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_wx_id(self, s: str, expected: bool):
        p = re.compile(r'(' + re_pattern.WX_ID + r')$')
        m = p.match(s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_qq_id(self, s: str, expected: bool):
        m = re.match(r'(' + re_pattern.QQ_ID + r')$', s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_phone_cn(self, s: str, expected: bool):
        m = re.match(r'(' + re_pattern.PHONE_CN + r')$', s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None

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
    def test_id_cn(self, s: str, expected: bool):
        m = re.match(r'(' + re_pattern.ID_CN + r')$', s)
        if expected:
            assert isinstance(m, re.Match)
        else:
            # not match
            assert m is None
