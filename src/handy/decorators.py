"""Decorators."""

from typing import Any


def attrs(**_kwargs: Any) -> Any:
    """Add attributes to a function/method.

    Usage:

        @attrs(any_attr=1, author='Lee')
        def func(*args, **kwargs):
            pass
    """

    def wrapper(_func: Any):
        """wrapper function."""
        for k, v in _kwargs.items():
            setattr(_func, k, v)
        return _func

    return wrapper
