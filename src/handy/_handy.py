import multiprocessing
import re
import string
from collections import defaultdict
from collections.abc import ItemsView, Iterator
from typing import Any, Callable, Literal, Union

from .re_pattern import (
    CN_CHAR,
    DOMAIN_NAMES,
    EMAIL,
    FLOAT_NUMBER,
    HTML,
    ID_CN,
    LANGUAGE,
    LICENSE_PLATES,
    PHONE_CN,
    QQ_ID,
    RGB_HEX,
    WX_ID,
    IPv4,
)


def find_chinese_characters(
    s: str, iterred: bool = True
) -> Union[Iterator[re.Match[str]], list[str]]:
    """Find Chinese characters."""
    p = re.compile(CN_CHAR)
    return p.finditer(s) if iterred else p.findall(s)


def validate_float_number(s: str) -> bool:
    """Float number validator."""
    return _validate_by_regex(s, FLOAT_NUMBER)


def validate_ipv4(s: str) -> bool:
    """IPv4 addresses validator."""
    return _validate_by_regex(s, IPv4)


def validate_email(s: str) -> bool:
    """Email address validator."""
    return _validate_by_regex(s, EMAIL, re.IGNORECASE)


def validate_html(s: str) -> bool:
    """HTML elements or tags validator."""
    return _validate_by_regex(s, HTML, re.IGNORECASE | re.DOTALL)


def validate_domain_name(s: str, language: LANGUAGE = LANGUAGE.EN) -> bool:
    """Domain name validator."""
    dn = DOMAIN_NAMES[language]
    m = re.match(r'(' + dn[0] + r')$', s, re.IGNORECASE)
    if m:
        return len(s) <= dn[1]
    return False


def validate_rgb_hex(s: str) -> bool:
    """Color RGB hex validator."""
    return _validate_by_regex(s, RGB_HEX, re.IGNORECASE)


def validate_password_strength(s: str, min_len: int) -> bool:
    """Password strength validator.

    包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符
    """
    if min_len < 2:
        raise ValueError('minimal length of password must greater than 1')
    m = re.match(
        r'.*(?=.{'
        + str(min_len)
        + r',})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*? ]).*$',
        s,
    )
    return m is not None


def validate_license_plate(s: str, region: Literal['cn', 'hk']) -> bool:
    """License plate validator."""
    return _validate_by_regex(s, LICENSE_PLATES[region])


def validate_wx_id(s: str) -> bool:
    """Wechat(Wexin) ID validator."""
    return _validate_by_regex(s, WX_ID)


def validate_qq_id(s: str) -> bool:
    """QQ ID validator."""
    return _validate_by_regex(s, QQ_ID)


def validate_phone_cn(s: str) -> bool:
    """Chinese phone number validator."""
    return _validate_by_regex(s, PHONE_CN)


def validate_id_cn(s: str) -> bool:
    """Chinese ID validator."""
    return _validate_by_regex(s, ID_CN)


def ispunctuation(s: str) -> bool:
    """Return `True` if all characters in `s` are ASCII punctuation characters
    in the C locale."""
    if not s:
        return False
    for c in s:
        if c not in string.punctuation:
            return False
    return True


class LocalMapReduce:
    """A lcoal (not distributed) version of MapReduce.

    Usage:

        mapper = LocalMapReduce(map_func, reduce_func)
        outputs: list[tuple[str, Any]] = mapper(inputs)
    """

    def __init__(
        self,
        map_func: Callable[
            [Any],
            tuple[Any, Any],
        ],
        reduce_func: Callable[
            [Any],
            tuple[Any, Any],
        ],
        workers: int = multiprocessing.cpu_count(),
    ) -> None:
        """
        @param map_func: Function to map inputs to intermediate data. Takes as argument
                         one input value and returns a tuple with the key and a value
                         to be reduced.
        @param reduce_func: Function to reduce partitioned version of intermediate data
                            to final output. Takes as argument a key as produced by
                            `map_func` and a sequence of the values associated with that
                            key.
        @param workers: The number of workers to create in the pool. Defaults to the
                        number of CPUs available on the current host.
        """
        self._map_func = map_func
        self._reduce_func = reduce_func
        self._pool = multiprocessing.Pool(workers)

    def __call__(
        self, inputs: Iterator[Any], chunksize: int = 1
    ) -> list[tuple[Any, Any]]:
        """Process the inputs through the map and reduce functions given.

        @param inputs: An iterable containing the input data to be processed.
        @param chunksize: The portion of the input data to hand to each worker.
                          This can be used to tune performance during the mapping
                          phase.
        """
        map_responses = self._pool.map(self._map_func, inputs, chunksize=chunksize)
        partition_data = self.partition(iter(map_responses))
        return self._pool.map(self._reduce_func, partition_data)

    def partition(
        self, mapped_values: Iterator[tuple[Any, Any]]
    ) -> ItemsView[Any, list[Any]]:
        """Organize the mapped values by their key.
        Returns an unsorted sequence of tuples with a key and a sequence of values.
        """
        partition_data: defaultdict[Any, list[Any]] = defaultdict(list)
        for key, value in mapped_values:
            partition_data[key].append(value)
        return partition_data.items()


def _validate_by_regex(s: str, pattern: str, flags: int = 0) -> bool:
    """Validator by Regex."""
    m = re.match(r'(' + pattern + r')$', s, flags=flags)
    return m is not None
