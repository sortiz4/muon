# Muon
Muon is a composable text generation framework designed to replace or
supplement traditional templating engines and improves on traditional issues
such as performance, readability, modularity, and testability.

## Installation
Muon can be installed through your package manager of choice using this GitHub
repository. Installation through `poetry` is shown below as an example.

```sh
$ poetry add git+https://github.com/sortiz4/muon.git
```

## Elements
The simplest type in Muon is an element. Elements can defined by extending an
`Element` and overriding it's `render` method, or decorating a function with
`element`. Elements must return an element, a string, an iterable, or `None`.

```python
from muon import element
from muon import Element
from muon import Renderable


class Key(Element):

    def __init__(self, name: str | None = None) -> None:
        self.name = name

    def render(self) -> Renderable:
        if self.name is not None:
            return '[[{}]]'.format(self.name)


@element
def Key(name: str | None = None) -> Renderable:
    if name is not None:
        return '[[{}]]'.format(name)
```

The class, `HtmlElement`, and the decorator, `html_element`, will automatically
escape simple strings not marked by `Raw` and are therefore recommended when
generating HTML documents.

```python
from muon import html_element
from muon import HtmlElement
from muon import Renderable


class Slot(HtmlElement):

    def __init__(self, name: str | None = None) -> None:
        self.name = name

    def render(self) -> Renderable:
        if self.name is not None:
            return '<{}>'.format(self.name)


@html_element
def Slot(name: str | None = None) -> Renderable:
    if name is not None:
        return '<{}>'.format(name)
```

All HTML tags have been aliased and converted to HTML elements. The full list
can be seen [here][1].

Attributes can be passed as named arguments to any HTML element (underscores in
attribute names will be converted to hyphens). Most attribute values will be
converted into a string or, in the case of booleans, reduced to a simpler
representation. However, three special attributes exist...

`children` represents the children of an element and must match the return type
of an element. `classes` will appear as `class` on elements and must be a
string or an iterable of strings (non-strings will be filtered out). `style`
must be a dictionary. Like attributes, underscores in property names will be
converted to hyphens.

## Rendering
The `render` function is the recommended way to render the root element. If
Django is installed, this function will return an `HttpResponse`.

```python
from app.templates import Document
from django.http import HttpRequest
from django.http import HttpResponse
from muon import render


def view(request: HttpRequest) -> HttpResponse:
    return render(Document)
```

## Example
A more complete example can be seen [here][2].

[1]: https://github.com/sortiz4/muon/blob/master/muon/core.py#L22
[2]: https://github.com/sortiz4/muon/blob/master/example.py
