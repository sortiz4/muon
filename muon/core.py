from __future__ import annotations
from typing import Iterable
from typing import Protocol

__all__ = [
    'Node',
    'Renderable',
]


class Node(Protocol):

    def render(self) -> Renderable:
        pass

    def __str__(self) -> str:
        pass


Renderable = str | Node | Iterable[str | Node] | None
