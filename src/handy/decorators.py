"""Decorators."""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, Type, Union

from . import LOGGER_NAME


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
    *types: Union[Type[object], tuple[Type[object], ...]],
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
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError(f'arg {a} ({type(a)}) does not match {t}')
            return _func(*args, **kwargs)

        return wrapper

    return _decorator


def returns(*rtype: Type[object]) -> Any:
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


def singleton(cls: Type[object]):
    """Define a class with a singleton instance.

    Usage:

        @singleton
        class MyClass:
            pass
    """
    instances: dict[Type[object], object] = {}

    def getinstance() -> object:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


def logging_wall_time(_func: Callable[..., Any]):
    """Logging the run time (wall time) of the decorated function in seconds."""
    logger = logging.getLogger(LOGGER_NAME)

    @wraps(_func)
    def wrapper(*args: Any, **kwargs: Any):
        start_time = time.perf_counter()
        result = _func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        logger.debug(f'Finished {_func.__name__}() in {run_time:.4f} seconds')
        return result

    return wrapper


def logging_wall_time_ns(_func: Callable[..., Any]):
    """Logging the run time (wall time) of the decorated function in nanoseconds."""
    logger = logging.getLogger(LOGGER_NAME)

    @wraps(_func)
    def wrapper(*args: Any, **kwargs: Any):
        start_time = time.perf_counter_ns()
        result = _func(*args, **kwargs)
        run_time = time.perf_counter_ns() - start_time
        logger.debug(f'Finished {_func.__name__}() in {run_time} nanoseconds')
        return result

    return wrapper


def logging_cpu_time(_func: Callable[..., Any]):
    """Logging the process time (CPU time) of the decorated function in seconds."""
    logger = logging.getLogger(LOGGER_NAME)

    @wraps(_func)
    def wrapper(*args: Any, **kwargs: Any):
        start_time = time.process_time()
        result = _func(*args, **kwargs)
        run_time = time.process_time() - start_time
        logger.debug(f'Finished {_func.__name__}() in {run_time:.4f} seconds')
        return result

    return wrapper


def logging_cpu_time_ns(_func: Callable[..., Any]):
    """Logging the process time (CPU time) of the decorated function in nanoseconds."""
    logger = logging.getLogger(LOGGER_NAME)

    @wraps(_func)
    def wrapper(*args: Any, **kwargs: Any):
        start_time = time.process_time_ns()
        result = _func(*args, **kwargs)
        run_time = time.process_time_ns() - start_time
        logger.debug(f'Finished {_func.__name__}() in {run_time} nanoseconds')
        return result

    return wrapper
