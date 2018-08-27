from typing import Callable, Generic, TypeVar, Optional
from abc import ABCMeta, abstractmethod

T = TypeVar('T')
S = TypeVar('S')
TCaller = Callable[[T], S]
TReturner = Callable[..., T]


class Monad(Generic[T]):
    __metaclass__ = ABCMeta

    def __init__(self, value: T) -> None:
        self._value = value or None

    @property
    def value(self) -> Optional[T]:
        return self._value

    @abstractmethod
    def bind(self, f: TCaller) -> 'Monad[S]':
        pass
