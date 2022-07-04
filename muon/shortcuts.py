from muon.core import Renderable
from typing import Any
from typing import Callable

try:
    from django.http import HttpResponse
except ImportError:
    def HttpResponse(value: Any) -> str:
        return str(value) if not isinstance(value, str) else value

__all__ = [
    'render',
]


def render(element: Callable[..., Renderable], **kwargs: Any) -> HttpResponse:
    return HttpResponse(element(**kwargs))
