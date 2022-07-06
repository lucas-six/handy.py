from typing import Any, Callable, Union

import pytest

from src.handy.decorators import accepts, attrs, returns, singleton


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
