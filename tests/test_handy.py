import random
import re
import string

import pytest

from src.handy import find_chinese_characters, is_domain_en, ispunctuation, re_pattern


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
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 3) // 2),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 3) // 2),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                False,
            ),
            ('123.dd', 1, True),
            (
                ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(1, re_pattern.DOMAIN_EN_MAX_LEN - 3),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + '.'
                + ''.join(random.choices(string.ascii_letters, k=2)),
                10000,
                False,
            ),
            ('abc.dd', 1, True),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 3),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 3),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 3),
                    )
                ),
                10000,
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
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
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 2) // 2),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.digits,
                        k=random.randint(2, (re_pattern.DOMAIN_EN_MAX_LEN - 2) // 2),
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
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 2),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 2),
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
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 2),
                    )
                )
                + '-.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 2),
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
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 2) // 3),
                    )
                )
                + '-'
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 2) // 3),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, (re_pattern.DOMAIN_EN_MAX_LEN - 2) // 3),
                    )
                ),
                10000,
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + '-'
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
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
            ('a-b-c.org', 1, True),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 4),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits + '-',
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 4),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(1, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 4),
                    )
                )
                + '.'
                + ''.join(
                    random.choices(
                        string.ascii_letters,
                        k=random.randint(2, (re_pattern.DOMAIN_EN_MAX_LEN - 1) // 4),
                    )
                ),
                10000,
                True,
            ),
            (
                ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits + '-',
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
                    )
                )
                + ''.join(
                    random.choices(
                        string.ascii_letters + string.digits,
                        k=random.randint(
                            re_pattern.DOMAIN_EN_MAX_LEN,
                            re_pattern.DOMAIN_EN_MAX_LEN + 1,
                        ),
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
        ),
    )
    def test_is_domain_en(self, s: str, times: int, expected: bool):
        while times:
            if times > 1:
                random.seed(times)
            if expected:
                assert is_domain_en(s)
            else:
                # not match
                assert not is_domain_en(s)
            times -= 1

    def test_ispunctuation(self):
        assert not ispunctuation('')

        for c in string.printable:
            if c in string.punctuation:
                assert ispunctuation(c)
            else:
                assert not ispunctuation(c)
