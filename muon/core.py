import html
from collections.abc import Iterable

__all__ = [
    'DocType',
    'element',
    'Element',
    'html_element',
    'HtmlElement',
    'Raw',
]

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
ALIASES = {
    'classes': 'class',
}


def _kebab(value):
    """
    Converts a snake case string to kebab case.
    """
    return value.lower().replace(UNDERSCORE, MINUS)


def _escape(value, quote):
    """
    Escapes HTML characters in plain strings (quotes are optional).
    """
    if type(value) is str:
        return html.escape(value, quote)
    return value


def _escape_attribute(value):
    """
    Escapes HTML characters in plain strings (including quotes).
    """
    return _escape(value, True)


def _escape_html(value):
    """
    Escapes HTML characters in plain strings (excluding quotes).
    """
    return _escape(value, False)


def _render_core(children):
    """
    Renders the children of an element.
    """
    if children is None:
        return EMPTY
    elif isinstance(children, str):
        return children
    elif isinstance(children, Iterable):
        return EMPTY.join(map(_render_core, children))
    return str(children)


def _render_html(children):
    """
    Safely renders the children of an HTML element.
    """
    if children is None:
        return EMPTY
    elif isinstance(children, str):
        return _escape_html(children)
    elif isinstance(children, Iterable):
        return EMPTY.join(map(_render_html, children))
    return str(children)


def _render_html_attribute(key, value):
    """
    Safely renders an attribute-value pair of an HTML element.
    """
    if value is not None:
        return '{}="{}"'.format(_escape_attribute(key), _escape_attribute(value))
    return _escape_attribute(key)


def _render_html_attributes(attributes):
    """
    Safely renders attribute-value pairs of an HTML element.
    """
    if attributes and isinstance(attributes, dict):
        def reduce_attributes():
            return [render_attribute(render_attribute_key(k), v) for k, v in attributes.items() if not should_skip(v)]

        def render_attribute(key, value):
            return _render_html_attribute(key, render_attribute_value(key, value))

        def render_attribute_key(key):
            # Map and case converts keys
            return _kebab(ALIASES.get(key, key))

        def render_attribute_value(key, value):
            if key == CLASS:
                # Reduce class values
                if not isinstance(value, str) and isinstance(value, Iterable):
                    return _render_html_class(*value)

            elif key == STYLE:
                # Reduce style values
                if isinstance(value, dict):
                    return _render_html_style(value)

            # Reduce boolean values
            if isinstance(value, bool):
                if value:
                    return None

            # Nothing to do
            return value

        def should_skip(value):
            return isinstance(value, bool) and not value

        return SPACE + SPACE.join(reduce_attributes())
    return EMPTY


def _render_html_class(*names):
    """
    Renders the list of class names of an HTML element.
    """
    return SPACE.join([name for name in names if isinstance(name, str)])


def _render_html_style(style):
    """
    Renders the inline style of an HTML element.
    """
    return SEMICOLON.join([COLON.join([_kebab(k), v]) for k, v in style.items()])


def element(closure):
    """
    A decorator for defining functional elements.
    """
    def wrapper(**kwargs):
        return _render_core(closure(**kwargs))
    return wrapper


def html_element(closure):
    """
    A decorator for defining functional HTML elements.
    """
    def wrapper(**kwargs):
        return Raw(_render_html(closure(**kwargs)))
    return wrapper


class Raw(str):
    pass


class Element:

    def render(self):
        raise NotImplementedError

    def __str__(self):
        return _render_core(self.render())


class DocType(Element):

    def __init__(self, dtd=None):
        self.dtd = dtd

    def render(self):
        def get_dtd():
            if isinstance(self.dtd, str):
                return _escape_html(self.dtd)
            return 'html'

        return '<!DOCTYPE{}>'.format(SPACE + get_dtd())


class HtmlElement(Element):

    def __init__(self, tag=None, void=False, children=None, **attributes):
        self.tag = tag
        self.void = void
        self.children = children
        self.attributes = attributes

    def render(self):
        def get_format():
            if self.void:
                return '<{tag}{attributes}/>'
            return '<{tag}{attributes}>{children}</{tag}>'

        options = {
            'tag': self.tag,
            'children': _render_html(self.children),
            'attributes': _render_html_attributes(self.attributes),
        }

        return Raw(get_format().format(**options))

    def __str__(self):
        return _render_html(self.render())
