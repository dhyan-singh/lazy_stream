from dataclasses import dataclass
from typing import Callable, Generic
from abc import ABC, abstractmethod
from itertools import islice

class Stream[T](ABC):
    @abstractmethod
    def head(self) -> T:
        pass

    @abstractmethod
    def tail(self) -> "Stream[T]":
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    def of(*l):
        if l:
            return Stream.cons(lambda: l[0], lambda: Stream.of(*l[1:]))
        else:
            return Empty[T]()

    def cons(hd: Callable[[], T], tl: Callable[[], "Stream[T]"]):
        return Cons(hd, tl)

    def toList(self) -> list[T]:
        # let's just consume here
        l = []
        n = self
        while isinstance(n, Cons):
            l.append(n.head()())
            n = n.tail()()
        return l

        # print(self.head()())
        # print(self.tail()().head()())
        # print(self.tail()().tail()().tail().head()())


class Empty[T](Stream[T]):
    def head(self) -> T:
        raise Exception("Empty Stream")
    
    def tail(self) -> "Stream[T]":
        raise Exception("Empty Stream")
    
    def is_empty(self) -> bool:
        return True

@dataclass
class Cons[T](Stream[T]):
    def __init__(self, head: Callable[[], T], tail: Callable[[], Stream[T]]):
        self._head = head
        self._tail = tail

    def head(self) -> T:
        return self._head
    
    def tail(self) -> "Stream[T]":
        return self._tail
    
    def is_empty(self) -> bool:
        return False

def lazy():
    yield 5

if __name__ == "__main__":
    # Cons[int](lambda: 5, lambda: Empty[int]())
    print(Stream[int].of(5, 7, 3, 4).toList())
    # Stream[int].of()