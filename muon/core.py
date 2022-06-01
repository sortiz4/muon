import html
from collections.abc import Iterable
from functools import wraps

__all__ = [
    'DocType',
    'element',
    'Element',
    'Heading',
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
        def map_key(key):
            # Map and case converts keys
            return _kebab(ALIASES.get(key, key))

        def map_value(key, value):
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

        def reduce_attributes():
            return [render_attribute(map_key(k), v) for k, v in attributes.items() if not should_skip(v)]

        def render_attribute(key, value):
            return _render_html_attribute(key, map_value(key, value))

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


def _add_html_elements(*tags):
    """
    Adds basic HTML element types to this module.
    """
    global __all__

    def get_methods(tag, void):
        def __init__(self, **kwargs):
            HtmlElement.__init__(self, **kwargs, tag=tag, void=void)
        return {'__init__': __init__}

    def get_types():
        for tag, name, void in tags:
            yield type(name if name is not None else tag.capitalize(), (HtmlElement,), get_methods(tag, void))

    # Construct the types
    types = {type.__name__: type for type in get_types()}

    # Update the exports
    __all__ += [*types.keys()]

    # Update the module
    globals().update(types)


def element(callback):
    """
    A decorator for defining functional elements.
    """
    @wraps(callback)
    def wrapper(**kwargs):
        return _render_core(callback(**kwargs))
    return wrapper


def html_element(callback):
    """
    A decorator for defining functional HTML elements.
    """
    @wraps(callback)
    def wrapper(**kwargs):
        return Raw(_render_html(callback(**kwargs)))
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


class Heading(HtmlElement):

    def __init__(self, size=1, **kwargs):
        super().__init__(**kwargs, tag='h{}'.format(size))


_add_html_elements(
    ('a', 'Anchor', False),
    ('abbr', 'Abbreviation', False),
    ('address', None, False),
    ('area', None, True),
    ('article', None, False),
    ('aside', None, False),
    ('audio', None, False),
    ('b', 'Bold', False),
    ('base', None, True),
    ('bdi', 'BidirectionalIsolate', False),
    ('bdo', 'BidirectionalOverride', False),
    ('blockquote', 'BlockQuote', False),
    ('body', None, False),
    ('br', 'Break', True),
    ('button', None, False),
    ('canvas', None, False),
    ('caption', None, False),
    ('cite', None, False),
    ('code', None, False),
    ('col', 'Column', True),
    ('colgroup', 'ColumnGroup', False),
    ('data', None, False),
    ('datalist', 'DataList', False),
    ('dd', 'DescriptionItem', False),
    ('del', 'Deleted', False),
    ('details', None, False),
    ('dfn', 'Definition', False),
    ('dialog', None, False),
    ('div', 'Block', False),
    ('dl', 'DescriptionList', False),
    ('dt', 'DescriptionTerm', False),
    ('em', 'Emphasis', False),
    ('embed', None, True),
    ('fieldset', 'FieldSet', False),
    ('figcaption', 'FigureCaption', False),
    ('figure', None, False),
    ('footer', None, False),
    ('form', None, False),
    ('head', None, False),
    ('header', None, False),
    ('hgroup', 'HeaderGroup', False),
    ('hr', 'Rule', True),
    ('html', None, False),
    ('i', 'Italic', False),
    ('iframe', None, False),
    ('img', 'Image', True),
    ('input', None, True),
    ('ins', 'Inserted', False),
    ('kbd', 'Keyboard', False),
    ('label', None, False),
    ('legend', None, False),
    ('li', 'ListItem', False),
    ('link', None, True),
    ('main', None, False),
    ('map', None, False),
    ('mark', None, False),
    ('menu', None, False),
    ('meta', None, True),
    ('meter', None, False),
    ('nav', 'Navigation', False),
    ('noscript', 'NoScript', False),
    ('object', None, False),
    ('ol', 'OrderedList', False),
    ('optgroup', 'OptionGroup', False),
    ('option', None, False),
    ('output', None, False),
    ('p', 'Paragraph', False),
    ('param', 'Parameter', True),
    ('picture', None, False),
    ('pre', 'Preformatted', False),
    ('progress', None, False),
    ('q', 'Quote', False),
    ('rb', 'RubyBase', False),
    ('rp', 'RubyParenthesis', False),
    ('rt', 'RubyText', False),
    ('rtc', 'RubyTextContainer', False),
    ('ruby', None, False),
    ('s', 'Strikethrough', False),
    ('samp', 'Sample', False),
    ('script', 'Script', False),
    ('section', None, False),
    ('select', None, False),
    ('slot', None, False),
    ('small', None, False),
    ('source', None, True),
    ('span', 'Inline', False),
    ('strong', None, False),
    ('style', None, False),
    ('sub', 'Subscript', False),
    ('summary', None, False),
    ('sup', 'Superscript', False),
    ('table', None, False),
    ('tbody', 'TableBody', False),
    ('td', 'TableCell', False),
    ('template', None, False),
    ('textarea', 'TextArea', False),
    ('tfoot', 'TableFoot', False),
    ('th', 'TableHeadCell', False),
    ('thead', 'TableHead', False),
    ('time', None, False),
    ('title', None, False),
    ('tr', 'TableRow', False),
    ('track', None, True),
    ('u', 'Underline', False),
    ('ul', 'UnorderedList', False),
    ('var', 'Variable', False),
    ('video', None, False),
    ('wbr', 'WordBreak', True),
)
