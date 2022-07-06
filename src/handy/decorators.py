"""Decorators."""

from functools import wraps
from typing import Any, Callable, Union


def attrs(**_kwargs: Any) -> Any:
    """Add attributes to a function/method.

    Usage:

        @attrs(any_attr=1, author='Lee')
        def func(*args, **kwargs):
            pass
    """

    def wrapper(_func: Callable[..., Any]):
        """wrapper function."""
        for k, v in _kwargs.items():
            setattr(_func, k, v)
        return _func

    return wrapper


def accepts(
    *types: Union[Any, tuple[Any, ...]],
) -> Any:
    """Enforce function argument type.

    Usage:

        @accepts(int, (int, float))
        def func(arg1, arg2):
            pass
    """

    def _decorator(_func: Callable[..., Any]):

        if len(types) != _func.__code__.co_argcount:
            raise TypeError('invalid number of arguments')

        @wraps(_func)
        def wrapper(*args: Any, **kwargs: Any):
            """wrapper function."""
            for (a, t) in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError(f'arg {a} ({type(a)}) does not match {t}')
            return _func(*args, **kwargs)

        return wrapper

    return _decorator


def returns(*rtype: Any) -> Any:
    """Enforce function return types.

    Usage:

        @returns(int)
        def func(arg1: int, arg2: int) -> int:
            return arg1 + arg2
    """

    def _decorator(_func: Callable[..., Any]):
        @wraps(_func)
        def wrapper(*args: Any, **kwargs: Any):
            """wrapper function."""
            result = _func(*args, **kwargs)
            if not isinstance(result, rtype):
                raise TypeError(f'return value {result} does not match {rtype}')
            return result

        return wrapper

    return _decorator


def singleton(cls: Any):
    """Define a class with a singleton instance.

    Usage:

        @singleton
        class MyClass:
            pass
    """
    instances: dict[Any, object] = {}

    def getinstance() -> object:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance
