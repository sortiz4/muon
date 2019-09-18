try:
    from django.http import HttpResponse
except ImportError:
    HttpResponse = lambda value: value


def render(element, **kwargs):
    return HttpResponse(element(**kwargs))
