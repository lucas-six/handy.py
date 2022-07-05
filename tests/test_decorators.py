from typing import Any, Callable

import pytest

from src.handy.decorators import attrs


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
        def func_arguments(*args: Any):
            '''attrs_func for testing.'''
            return 9 + args[0]

        return func_arguments

    def test_attrs(
        self,
        attrs_func_no_argument: Callable[[], None],
        attrs_func_with_arguments: Callable[[Any], None],
    ):
        assert attrs_func_no_argument.__name__ == 'func'
        assert attrs_func_no_argument.__doc__ == 'attrs_func for testing.'
        assert attrs_func_no_argument.any_attr_1 == 1
        assert attrs_func_no_argument.any_attr_2 == '2'
        assert attrs_func_no_argument() == 9

        assert attrs_func_with_arguments.__name__ == 'func_arguments'
        assert attrs_func_with_arguments.__doc__ == 'attrs_func for testing.'
        assert attrs_func_with_arguments.any_attr_1 == 3
        assert attrs_func_with_arguments.any_attr_2 == '4'
        assert attrs_func_with_arguments(1) == 9 + 1
