from functools import partial
from typing import Generic, Union, Callable, Type, Optional, TypeVar

from .monad import T, Monad, TCaller

EitherFunc = Callable[[T], 'Either']
TReturner = Callable[..., T]
EitherTOrS = Union['Either[Optional[S]]', 'Either[T]']


class Either(Monad, Generic[T]):

    # Initializers

    def __init__(self, value: T, error: Exception=None) -> None:
        super().__init__(value)
        self._error = error or None

    @classmethod
    def fromfunction(cls, f: TReturner, *args) -> 'Either[Optional[T]]':
        try:
            value = f(*args)
            return cls(value)
        except Exception as e:
            return cls(None, e)

    @classmethod
    def frompartialfunction(cls, f: TReturner) -> EitherFunc:
        return partial(Either.fromfunction, f)

    # Getters

    @property
    def error(self) -> Optional[Exception]:
        return self._error

    @property
    def error_type(self) -> Type:
        return type(self._error)

    # Public instance methods

    def call(self, f: TCaller) -> EitherTOrS:
        if self._error is not None or self._value is None:
            return self
        return Either(f(self._value))

    def try_call(self, f: TCaller) -> EitherTOrS:
        try:
            return self.call(f)
        except Exception as e:
            return Either(None, e)

    @staticmethod
    def try_call_partial(f: TCaller) -> EitherFunc:
        def _inner(f: TCaller, either: Either):
            return either.try_call(f)

        return partial(_inner, f)
