import logging
from collections.abc import Callable
from typing import Any, Literal, Union

import pytest

from src.handy import LOGGER_NAME
from src.handy.decorators import (
    accepts,
    attrs,
    logging_cpu_time,
    logging_cpu_time_ns,
    logging_wall_time,
    logging_wall_time_ns,
    returns,
    singleton,
)


class TestDecorators:
    @pytest.fixture
    def attrs_func_no_argument(self):
        @attrs(any_attr_1=1, any_attr_2='2')
        def func():
            '''attrs_func for testing.'''
            return 9

        return func

    @pytest.fixture
    def attrs_func_with_arguments(self):
        @attrs(any_attr_1=3, any_attr_2='4')
        def func(*args: Any):
            '''attrs_func for testing.'''
            return 9 + args[0]

        return func

    def test_attrs(
        self,
        attrs_func_no_argument: Any,
        attrs_func_with_arguments: Any,
    ):
        assert attrs_func_no_argument.__name__ == 'func'
        assert (
            attrs_func_no_argument.__qualname__
            == f'{self.__class__.__name__}.attrs_func_no_argument.<locals>.func'
        )
        assert attrs_func_no_argument.__doc__ == 'attrs_func for testing.'
        assert attrs_func_no_argument.any_attr_1 == 1
        assert attrs_func_no_argument.any_attr_2 == '2'
        assert attrs_func_no_argument() == 9

        assert attrs_func_with_arguments.__name__ == 'func'
        assert (
            attrs_func_with_arguments.__qualname__
            == f'{self.__class__.__name__}.attrs_func_with_arguments.<locals>.func'
        )
        assert attrs_func_with_arguments.__doc__ == 'attrs_func for testing.'
        assert attrs_func_with_arguments.any_attr_1 == 3
        assert attrs_func_with_arguments.any_attr_2 == '4'
        assert attrs_func_with_arguments(1) == 9 + 1

    @pytest.fixture
    def accepts_func(self):
        @accepts(int, (int, float))
        def func(arg1: int, arg2: float) -> float:
            '''accepts_func for testing.'''
            return arg1 * arg2

        return func

    def test_accepts_attributes(self, accepts_func: Callable[[int, float], float]):
        assert accepts_func.__name__ == 'func'
        assert (
            accepts_func.__qualname__
            == f'{self.__class__.__name__}.accepts_func.<locals>.func'
        )
        assert accepts_func.__doc__ == 'accepts_func for testing.'

        assert accepts_func(1, 2) == 2
        assert accepts_func(1, 2.2) == 2.2

    @pytest.mark.parametrize(
        ('arg1', 'arg2'),
        (('1', 2), ('1', 2.2), (1, '2'), ('1', '2')),
    )
    def test_accepts_invalid_arguments_type(
        self,
        accepts_func: Callable[[int, float], float],
        arg1: Union[str, float],
        arg2: Union[str, float],
    ):
        with pytest.raises(TypeError):
            accepts_func(arg1, arg2)  # type: ignore

    def test_accepts_invalid_number_of_arguments(self):
        with pytest.raises(TypeError, match='invalid number of arguments'):

            @accepts(int)
            def func1(arg1: int, arg2: float) -> float:
                '''accepts_func for testing.'''
                return arg1 * arg2

            assert func1(1, 2) == 2

        with pytest.raises(TypeError, match='invalid number of arguments'):

            @accepts(int, (int, float), str)
            def func2(arg1: int, arg2: float) -> float:
                '''accepts_func for testing.'''
                return arg1 * arg2

            assert func2(1, 2) == 2

        with pytest.raises(TypeError, match='invalid number of arguments'):

            @accepts()
            def func3(arg1: int, arg2: float) -> float:
                '''accepts_func for testing.'''
                return arg1 * arg2

            assert func3(1, 2) == 2

    @pytest.fixture
    def returns_func(self):
        @returns(int, float)
        def func(arg1: int, arg2: float) -> float:
            '''returns_func for testing.'''
            return arg1 * arg2

        return func

    def test_returns_attributes(self, returns_func: Callable[[int, float], float]):
        assert returns_func.__name__ == 'func'
        assert (
            returns_func.__qualname__
            == f'{self.__class__.__name__}.returns_func.<locals>.func'
        )
        assert returns_func.__doc__ == 'returns_func for testing.'

        assert returns_func(1, 2) == 2
        assert returns_func(1, 2.2) == 2.2

    @pytest.mark.parametrize(
        ('arg1', 'arg2'),
        (('1', 2), ('1', 2.2), (1, '2'), ('1', '2')),
    )
    def test_returns_invalid_return_type(
        self,
        returns_func: Callable[[int, float], float],
        arg1: Union[str, float],
        arg2: Union[str, float],
    ):
        with pytest.raises(TypeError):
            returns_func(arg1, arg2)  # type: ignore

    def test_singleton(self):
        @singleton
        class MyClass:
            pass

        c1 = MyClass()
        c2 = MyClass()
        assert c1 == c2
        assert c1 is c2

    @pytest.fixture
    def waste_wall_time_func(self):
        @logging_wall_time
        def waste_time(num_times: int):
            for _ in range(num_times):
                sum(i**2 for i in range(1000))
            return True

        return waste_time

    @pytest.fixture
    def waste_wall_time_ns_func(self):
        @logging_wall_time_ns
        def waste_time(num_times: int):
            for _ in range(num_times):
                sum(i**2 for i in range(1000))
            return True

        return waste_time

    @pytest.fixture
    def waste_cpu_time_func(self):
        @logging_cpu_time
        def waste_time(num_times: int):
            for _ in range(num_times):
                sum(i**2 for i in range(1000))
            return True

        return waste_time

    @pytest.fixture
    def waste_cpu_time_ns_func(self):
        @logging_cpu_time_ns
        def waste_time(num_times: int):
            for _ in range(num_times):
                sum(i**2 for i in range(1000))
            return True

        return waste_time

    def test_logging_wall_time(
        self, caplog: Any, waste_wall_time_func: Callable[[int], Literal[True]]
    ):
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            assert waste_wall_time_func(99)

        assert len(caplog.records) == 1
        assert caplog.records[0].message.startswith('Finished waste_time() in')
        assert caplog.records[0].message.endswith('seconds')
        assert caplog.records[0].levelno == logging.DEBUG

    def test_logging_wall_time_ns(
        self, caplog: Any, waste_wall_time_ns_func: Callable[[int], Literal[True]]
    ):
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            assert waste_wall_time_ns_func(99)

        assert len(caplog.records) == 1
        assert caplog.records[0].message.startswith('Finished waste_time() in')
        assert caplog.records[0].message.endswith('nanoseconds')
        assert caplog.records[0].levelno == logging.DEBUG

    def test_logging_cpu_time(
        self, caplog: Any, waste_cpu_time_func: Callable[[int], Literal[True]]
    ):

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            assert waste_cpu_time_func(99)

        assert len(caplog.records) == 1
        assert caplog.records[0].message.startswith('Finished waste_time() in')
        assert caplog.records[0].message.endswith('seconds')
        assert caplog.records[0].levelno == logging.DEBUG

    def test_logging_cpu_time_ns(
        self, caplog: Any, waste_cpu_time_ns_func: Callable[[int], Literal[True]]
    ):

        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            assert waste_cpu_time_ns_func(99)

        assert len(caplog.records) == 1
        assert caplog.records[0].message.startswith('Finished waste_time() in')
        assert caplog.records[0].message.endswith('nanoseconds')
        assert caplog.records[0].levelno == logging.DEBUG
