try:
    from django.http import HttpResponse
except ImportError:
    HttpResponse = lambda e: str(e) if not isinstance(e, str) else e

__all__ = ['render']


def render(element, **kwargs):
    return HttpResponse(element(**kwargs))
