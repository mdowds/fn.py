from functools import partial
from typing import Callable, Generic, TypeVar, Optional
from abc import ABCMeta, abstractmethod

T = TypeVar('T')
S = TypeVar('S')
TCaller = Callable[[T], S]
TCallerWrapped = Callable[['Monad[T]'], 'Monad[S]']


class Monad(Generic[T]):
    __metaclass__ = ABCMeta

    def __init__(self, value: T) -> None:
        self._value = value or None

    @property
    def value(self) -> Optional[T]:
        return self._value

    @abstractmethod
    def call(self, f: TCaller) -> 'Monad[S]': pass

    @staticmethod
    def call_partial(f: TCaller) -> TCallerWrapped:
        def __inner(f: TCaller, monad: Monad) -> 'Monad[S]':
            return monad.call(f)

        return partial(__inner, f)


