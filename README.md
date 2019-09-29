# Muon
Muon is a composable text generation framework designed to substitute or
supplement traditional templating engines with vanilla Python. This approach
eliminates the overhead associated with parsing (along with all ambiguities
therein) and improves on common issues such as performance, readability,
modularity, and testability.

# Usage

### Installation
Muon requires Python 3 and can be installed through your package manager of
choice using this GitHub repository. Installation through pip is shown below.

```sh
$ pip install git+https://github.com/sortiz4/muon.git#egg=muon
```

### Elements
The simplest type in Muon is an element. Elements can defined by extending an
`Element` and overriding it's render method, or decorating a function with
`element`. Elements must return an element, a string, an iterable, or `None`.

```python
from muon import element
from muon import Element


class Key(Element):

    def __init__(self, name=None):
        self.name = name

    def render(self):
        if self.name is not None:
            return '[[{}]]'.format(self.name)


@element
def Key(name=None):
    if name is not None:
        return '[[{}]]'.format(name)
```

The class, `HtmlElement`, and the decorator, `html_element`, will automatically
escape simple strings not marked by `Raw` and are therefore recommended when
generating HTML documents.

```python
from muon import html_element
from muon import HtmlElement


class Slot(HtmlElement):

    def __init__(self, name=None):
        self.name = name

    def render(self):
        if self.name is not None:
            return '<{}>'.format(self.name)


@html_element
def Slot(name=None):
    if name is not None:
        return '<{}>'.format(name)
```

All HTML tags have been aliased and converted to HTML elements. The full list
can be seen [here](https://github.com/sortiz4/muon/blob/master/muon/html.py#L58).

Attributes can be passed as named arguments to any HTML element (underscores in
attribute names will be converted to hyphens). Most attribute values will be
converted into a string or, in the case of booleans, reduced to a simpler
representation. However, three special attributes exist...

`children` represents the children of an element and must match the return
signature of an element.

`classname` will appear as `class` on elements and must be a string or an
iterable of strings (all non-strings will be filtered out).

`style` must be a dictionary. Like attributes, underscores in property names
will be converted to hyphens.

```python
```

### Channels
Channels can be used to alleviate the repetition associated with passing down
arguments to deeply nested elements. Channels accept a default value that is
only used when the channel has not been written to or the previous value has
been deleted.

```python
from muon import Channel
from muon import html_element
from muon import HtmlElement

count_channel = Channel(10)
label_channel = Channel('')


@html_element
def Parent(label='Node'):
    label_channel.write(label)
    count = count_channel.read()
    return [Child() for _ in range(count)]


@html_element
def Child():
    label = label_channel.read()
    return '<{}>'.format(label)
```

### Rendering
The `render` function is the recommended way to render the root element. If
Django is installed, this function will return an `HttpResponse`.

```python
from muon import render
from templates import Document


def view(request):
    return render(Document)
```

### Example
A more complete example can be seen [here](https://github.com/sortiz4/muon/blob/master/example.py).
