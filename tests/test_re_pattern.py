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
        p = re.compile(re_pattern.CN_CHAR)
        assert p.findall(s) == expected

    @pytest.mark.parametrize(
        ('s', 'times', 'expected'),
        (
            ('abc', 1, False),
            (
                ''.join(
                    random.choices(
                        string.printable.replace('.', ''),
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                ),
                10000,
                False,
            ),
            ('abc.', 1, False),
            (
                ''.join(
                    random.choices(
                        string.printable.replace('.', ''),
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.',
                10000,
                False,
            ),
            ('abc..', 1, False),
            (
                ''.join(
                    random.choices(
                        string.printable.replace('.', ''),
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '..',
                10000,
                False,
            ),
            ('abc.d', 1, False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + random.choice(string.ascii_letters),
                10000,
                False,
            ),
            ('abc$;.dd', 1, False),
            (
                ''.join(
                    random.choices(
                        string.printable.replace('.', ''),
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + ''.join(
                    random.choices(
                        string.punctuation.replace('.', ''),
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                False,
            ),
            ('abc.d;', 1, False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + random.choice(string.printable.replace('.', ''))
                + random.choice(string.punctuation),
                10000,
                False,
            ),
            ('123abc.dd', 1, True),
            (
                ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                True,
            ),
            ('123.dd', 1, True),
            (
                ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                True,
            ),
            ('abc.dd', 1, True),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                ),
                10000,
                True,
            ),
            ('abc.ddd.', 1, False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.',
                10000,
                False,
            ),
            ('abc.12', 1, False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.',
                10000,
                False,
            ),
            ('-abc.org', 1, False),
            (
                '-'
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                ),
                10000,
                False,
            ),
            ('abc-.org', 1, False),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '-.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                ),
                10000,
                False,
            ),
            ('a-bc.org', 1, True),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '-'
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                ),
                10000,
                True,
            ),
            ('a-b-c.org', 1, True),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits + '-',
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, re_pattern.DOMAIN_EN_MAX_LEN),
                    )
                ),
                10000,
                True,
            ),
        ),
    )
    def test_domain_en(self, s: str, times: int, expected: bool):
        p = re.compile(re_pattern.DOMAIN_EN + r'$', re.IGNORECASE)
        while times:
            if times > 1:
                random.seed(times)
            m = p.match(s)
            if expected:
                assert isinstance(m, re.Match)
            else:
                # not match
                assert m is None
            times -= 1
