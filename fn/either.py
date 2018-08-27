from typing import Generic, Type, Optional

from fn.monad import TReturner
from .monad import T, S, Monad, TCaller


class Either(Monad, Generic[T]):

    def __init__(self, value: T, error: Exception=None) -> None:
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

    def __rshift__(self, f: TCaller) -> 'Either[S]':
        """Overload >> operator for Either instances"""
        return self.bind(f)

    def bind(self, f: TCaller) -> 'Either[S]':
        """Try applying the given function, producing
        new instance containing either the new value
        or the error encountered"""
        try:
            if self._error is not None or self._value is None:
                return self
            return Either(f(self._value))
        except Exception as e:
            return Either(None, e)
