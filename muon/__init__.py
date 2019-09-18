import html
from collections.abc import Iterable

# Well-known strings
EMPTY = ''
SPACE = '\x20'
MINUS = '\x2D'
COLON = '\x3A'
SEMICOLON = '\x3B'
UNDERSCORE = '\x5F'

# Well-known attributes
STYLE = 'style'

# Well-known attribute aliases
ALIASES = {'class_name': 'class'}


def _snake_to_kebab(value):
    """
    Converts a string from snake case to kebab case.
    """
    return value.lower().replace(UNDERSCORE, MINUS)


def _escape(value, quote):
    """
    """
    if not isinstance(value, Raw):
        return html.escape(value, quote=quote)
    return value


def _escape_attribute(value):
    """
    """
    return _escape(value, True)


def _escape_children(value):
    """
    """
    return _escape(value, False)


def _render_style(style):
    kvs = []
    for k, v in style.items():
        kvs.append('{}:{}'.format(_snake_to_kebab(k), v))
    return SEMICOLON.join(kvs)


def _format_attribute(key, value):
    """
    """
    if value is not None:
        return '{}="{}"'.format(_escape_attribute(key), _escape_attribute(value))
    return _escape_attribute(key)


def _render_attributes(attributes):
    """
    """
    if attributes and isinstance(attributes, dict):
        kvs = []
        for k, v in attributes.items():
            # Map aliased keys
            if k in ALIASES:
                k = ALIASES[k]

            # Case convert keys
            k = _snake_to_kebab(k)

            # Reduce boolean values
            if isinstance(v, bool):
                if not v:
                    v = str(v).lower()
                else:
                    v = None

            # Reduce style values
            if k == STYLE:
                if isinstance(v, dict):
                    v = _render_style(v)

            # Append the key-value pair
            kvs.append([k, v])
        return SPACE + SPACE.join([_format_attribute(k, v) for k, v in kvs])
    return EMPTY


def _render_children(children):
    """
    """
    if isinstance(children, str):
        return _escape_children(children)
    elif isinstance(children, Element):
        return str(children)
    elif isinstance(children, Iterable):
        return EMPTY.join(map(_render_children, children))
    return EMPTY


def class_names(*args):
    """
    """
    return SPACE.join([arg for arg in args if isinstance(arg, str)])


class Raw(str):
    pass


class Element:

    def render(self):
        raise NotImplementedError

    def __str__(self):
        return _render_children(self.render())


class Fragment(Element):

    def __init__(self, children=None):
        self.children = children

    def render(self):
        return _render_children(self.children)


class DocType(Element):

    FORMAT = '<!DOCTYPE{}>'
    HTML5 = 'html'

    def __init__(self, data=None):
        self.data = data

    def render(self):
        if isinstance(self.data, str):
            data = _escape_children(self.data)
        else:
            data = self.HTML5
        return Raw(self.FORMAT.format(SPACE + data))


class HtmlElement(Element):

    FORMAT_A = '<{tag}{attributes}/>'
    FORMAT_B = '<{tag}{attributes}>{children}</{tag}>'

    def __init__(self, tag=None, children=None, **attributes):
        self.tag = tag
        self.children = children
        self.attributes = attributes

    def render(self):
        kwargs = {
            'tag': self.tag,
            'children': _render_children(self.children),
            'attributes': _render_attributes(self.attributes),
        }
        if kwargs['children']:
            FORMAT = self.FORMAT_B
        else:
            FORMAT = self.FORMAT_A
        return Raw(FORMAT.format(**kwargs))


class Block(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='div')


class Body(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='body')


class Head(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='head')


class Heading(HtmlElement):

    def __init__(self, size=1, **kwargs):
        super().__init__(**kwargs, tag='h{}'.format(size))


class Html(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='html')


class Inline(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='span')


class Input(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='input')


class Link(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='link')


class Meta(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='meta')


class NoScript(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='noscript')


class Script(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='script')
        self.FORMAT_A = self.FORMAT_B


class TextArea(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='textarea')


class Title(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='title')
