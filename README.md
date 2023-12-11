# Muon
Muon is a composable text generation framework designed to replace traditional
templating engines and improve common issues such as performance, readability,
modularity, and testability.

## Installation
Muon can be installed through your package manager of choice using this GitHub
repository. Installation through `poetry` is shown below as an example.

```sh
$ poetry add git+https://github.com/sortiz4/muon.git
```

## Elements
The simplest type in Muon is an element. Elements can be defined by extending
an `Element` and overriding the `render` method, or decorating a function with
`element`. Elements must return a [`Renderable`][1].

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

The `HtmlElement` class and `html_element` decorator will escape strings and
should be used when generating HTML documents. `Safe` strings can be used to
avoid escaping.

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
can be seen [here][2].

Attributes can be passed as named arguments to any HTML element (underscores in
attribute names will be replaced with hyphens). Most attribute values will be
converted into a string or, in the case of booleans, reduced to a simpler
representation. However, three special attributes exist...

- `children` represents the children of an element and must be a renderable.
- `classes` will appear as `class` on elements and must be a string or an
iterable of strings (other types will be omitted).
- `style` must be a dictionary of property names to values (underscores in
property names will also be replaced with hyphens).

## Example
A more complete example can be seen [here][3].

[1]: https://github.com/sortiz4/muon/blob/master/muon/core.py#L20
[2]: https://github.com/sortiz4/muon/blob/master/muon/elements.py#L24
[3]: https://github.com/sortiz4/muon/blob/master/example.py
