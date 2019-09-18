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
CLASS = 'class'
STYLE = 'style'

# Well-known attribute aliases
ALIASES = {'classname': 'class'}


def _kebab(value):
    """
    Converts a string to kebab case.
    """
    return value.lower().replace(UNDERSCORE, MINUS)


def _escape(value, quote):
    """
    """
    if type(value) is str:
        return html.escape(value, quote)
    return value


def _escape_attribute(value):
    """
    """
    return _escape(value, True)


def _escape_html(value):
    """
    """
    return _escape(value, False)


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
        entries = []
        for k, v in attributes.items():
            # Map aliased keys
            if k in ALIASES:
                k = ALIASES[k]

            # Case convert keys
            k = _kebab(k)

            if k == CLASS:
                # Reduce class values
                if not isinstance(v, str) and isinstance(v, Iterable):
                    v = _render_class(*v)

            elif k == STYLE:
                # Reduce style values
                if isinstance(v, dict):
                    v = _render_style(v)

            # Reduce boolean values
            if isinstance(v, bool):
                if v:
                    v = None
                else:
                    continue

            # Format the attribute
            entries.append(_format_attribute(k, v))
        return SPACE + SPACE.join(entries)
    return EMPTY


def _render_class(*args):
    """
    """
    return SPACE.join([arg for arg in args if isinstance(arg, str)])


def _render_core(children):
    """
    """
    if isinstance(children, str):
        return children
    elif isinstance(children, Element):
        return str(children)
    elif isinstance(children, Iterable):
        return EMPTY.join(map(_render_core, children))
    return EMPTY


def _render_html(children):
    """
    """
    if isinstance(children, str):
        return _escape_html(children)
    elif isinstance(children, Element):
        return str(children)
    elif isinstance(children, Iterable):
        return EMPTY.join(map(_render_html, children))
    return EMPTY


def _render_style(style):
    """
    """
    return SEMICOLON.join([COLON.join([_kebab(k), v]) for k, v in style.items()])


class Raw(str):
    pass


class Element:

    def render(self):
        raise NotImplementedError

    def __str__(self):
        return _render_core(self.render())


class DocType(Element):

    FORMAT = '<!DOCTYPE{}>'

    def __init__(self, dtd=None):
        self.dtd = dtd

    def render(self):
        if isinstance(self.dtd, str):
            dtd = _escape_html(self.dtd)
        else:
            dtd = 'html'
        return self.FORMAT.format(SPACE + dtd)


class HtmlElement(Element):

    FORMAT_A = '<{tag}{attributes}/>'
    FORMAT_B = '<{tag}{attributes}>{children}</{tag}>'

    def __init__(self, tag=None, children=None, **attributes):
        self.tag = tag
        self.children = children
        self.attributes = attributes

    def render(self):
        options = {
            'tag': self.tag,
            'children': _render_html(self.children),
            'attributes': _render_attributes(self.attributes),
        }
        if options['children']:
            FORMAT = self.FORMAT_B
        else:
            FORMAT = self.FORMAT_A
        return Raw(FORMAT.format(**options))

    def __str__(self):
        return _render_html(self.render())


class Block(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='div')


class Body(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='body')


class Break(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='br')


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


class Rule(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='hr')


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
