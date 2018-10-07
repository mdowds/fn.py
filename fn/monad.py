from typing import Callable, Generic, TypeVar, Optional, Type
from abc import ABCMeta, abstractmethod

T = TypeVar('T')
S = TypeVar('S')
TModifier = Callable[[T], S]
TReturner = Callable[..., T]


class Monad(Generic[T]):
    __metaclass__ = ABCMeta

    def __init__(self, value: T) -> None:
        self._value = value or None

    @property
    def value(self) -> Optional[T]:
        return self._value

    @abstractmethod
    def bind(self, f: TModifier) -> 'Monad[S]':
        pass


class Pipe(Monad, Generic[T]):
    """Provide simple syntax for piping values
    between single-parameter functions.

    Usage example:

    >>> val = Pipe(10) >> (_ + 10) >> (_ + 5)
    >>> print(val)
    25
    >>> val = Pipe(range(10)) >> (filter, _ < 6) >> sum
    >>> print(val)
    15
    """

    def __rshift__(self, f: TModifier) -> 'Pipe[S]':
        """Overload >> operator for Pipe instances"""
        return self.bind(f)

    def bind(self, f: TModifier) -> 'Pipe[S]':
        """Apply the given function, producing
        new instance containing the new value"""
        return Pipe(f(self.value))


class Either(Monad, Generic[T]):
    """Wrapper for values that could be an expected
    type or an error.

    Trying to apply further functions will cause them
    to be applied to values, or skipped for errors.

    Usage example:

    >>> val = Either(10) >> (_ + 10) >> (_ + 5)
    >>> print(val)
    25

    >>> def raiser(x): raise Exception()
    >>> val = Either(10) >> raiser >> (_ + 5)
    >>> if val.is_error:
    >>>     print(val.error)
    >>> else:
    >>>     print(val.value)
    Exception()
    """

    def __init__(self, value: T, error: Exception = None) -> None:
        super().__init__(value)
        self._error = error or None

    @classmethod
    def fromfunction(cls, f: TReturner, *args) -> 'Either[T]':
        """Create an instance from the function and
        args provided"""
        try:
            value = f(*args)
            return cls(value)
        except Exception as e:
            return cls(None, e)

    @property
    def error(self) -> Optional[Exception]:
        return self._error

    @property
    def error_type(self) -> Type:
        return type(self._error)

    @property
    def is_error(self) -> bool:
        return self._error is not None

    def __rshift__(self, f: TModifier) -> 'Either[S]':
        """Overload >> operator for Either instances"""
        return self.bind(f)

    def bind(self, f: TModifier) -> 'Either[S]':
        """Try applying the given function, producing
        new instance containing either the new value
        or the error encountered"""
        try:
            if self._error is not None or self._value is None:
                return self
            return Either(f(self._value))
        except Exception as e:
            return Either(None, e)
