import html
from functools import wraps
from muon.core import Renderable
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Mapping

__all__ = [
    # Utilities
    'Raw',

    # Decorators
    'element',
    'html_element',

    # Core Elements
    'Element',
    'HtmlElement',

    # Sgml Elements
    'DocType',

    # Html Elements
    'Anchor',
    'Abbreviation',
    'Address',
    'Area',
    'Article',
    'Aside',
    'Audio',
    'Bold',
    'Base',
    'BidirectionalIsolate',
    'BidirectionalOverride',
    'BlockQuote',
    'Body',
    'Break',
    'Button',
    'Canvas',
    'Caption',
    'Cite',
    'Code',
    'Column',
    'ColumnGroup',
    'Data',
    'DataList',
    'DescriptionItem',
    'Deleted',
    'Details',
    'Definition',
    'Dialog',
    'Block',
    'DescriptionList',
    'DescriptionTerm',
    'Emphasis',
    'Embed',
    'FieldSet',
    'FigureCaption',
    'Figure',
    'Footer',
    'Form',
    'Head',
    'Header',
    'Heading',
    'HeaderGroup',
    'Rule',
    'Html',
    'Italic',
    'Iframe',
    'Image',
    'Input',
    'Inserted',
    'Keyboard',
    'Label',
    'Legend',
    'ListItem',
    'Link',
    'Main',
    'Map',
    'Mark',
    'Menu',
    'Meta',
    'Meter',
    'Navigation',
    'NoScript',
    'Object',
    'OrderedList',
    'OptionGroup',
    'Option',
    'Output',
    'Paragraph',
    'Parameter',
    'Picture',
    'Preformatted',
    'Progress',
    'Quote',
    'RubyBase',
    'RubyParenthesis',
    'RubyText',
    'RubyTextContainer',
    'Ruby',
    'Strikethrough',
    'Sample',
    'Script',
    'Section',
    'Select',
    'Slot',
    'Small',
    'Source',
    'Inline',
    'Strong',
    'Style',
    'Subscript',
    'Summary',
    'Superscript',
    'Table',
    'TableBody',
    'TableCell',
    'Template',
    'TextArea',
    'TableFoot',
    'TableHeadCell',
    'TableHead',
    'Time',
    'Title',
    'TableRow',
    'Track',
    'Underline',
    'UnorderedList',
    'Variable',
    'Video',
    'WordBreak',
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
ALIASES = {'classes': CLASS}


def snake_to_kebab(value: str) -> str:
    """
    Converts a snake case string to kebab case.
    """
    return value.lower().replace(UNDERSCORE, MINUS)


def escape(value: Any, quote: bool) -> Any:
    """
    Escapes HTML characters in plain strings (quotes are optional).
    """
    if type(value) is str:
        return html.escape(value, quote)
    return value


def escape_attribute(value: Any) -> Any:
    """
    Escapes HTML characters in plain strings (including quotes).
    """
    return escape(value, True)


def escape_html(value: str) -> str:
    """
    Escapes HTML characters in plain strings (excluding quotes).
    """
    return escape(value, False)


def render_core(children: Renderable) -> str:
    """
    Renders the children of an element.
    """
    if children is None:
        return EMPTY
    elif isinstance(children, str):
        return children
    elif isinstance(children, Iterable):
        return EMPTY.join(map(render_core, children))
    return str(children)


def render_html(children: Renderable) -> str:
    """
    Safely renders the children of an HTML element.
    """
    if children is None:
        return EMPTY
    elif isinstance(children, str):
        return escape_html(children)
    elif isinstance(children, Iterable):
        return EMPTY.join(map(render_html, children))
    return str(children)


def render_html_attribute(key: str, value: Any) -> str:
    """
    Safely renders an attribute-value pair of an HTML element.
    """
    if value is not None:
        return '{}="{}"'.format(escape_attribute(key), escape_attribute(value))
    return escape_attribute(key)


def render_html_attributes(attributes: Mapping[str, Any]) -> str:
    """
    Safely renders attribute-value pairs of an HTML element.
    """
    if attributes and isinstance(attributes, dict):
        def map_key(key: str) -> str:
            # Map and case converts keys
            return snake_to_kebab(ALIASES.get(key, key))

        def map_value(key: str, value: Any) -> Any:
            if key == CLASS:
                # Reduce class values
                if not isinstance(value, str) and isinstance(value, Iterable):
                    return render_html_class(*value)

            elif key == STYLE:
                # Reduce style values
                if isinstance(value, dict):
                    return render_html_style(value)

            # Reduce boolean values
            if isinstance(value, bool):
                if value:
                    return None

            # Nothing to do
            return value

        def reduce_attributes() -> Iterable[str]:
            return [render_attribute(map_key(k), v) for k, v in attributes.items() if not should_skip(v)]

        def render_attribute(key: str, value: Any) -> str:
            return render_html_attribute(key, map_value(key, value))

        def should_skip(value: Any) -> bool:
            return isinstance(value, bool) and not value

        return SPACE + SPACE.join(reduce_attributes())
    return EMPTY


def render_html_class(*names: Any) -> str:
    """
    Renders the list of class names of an HTML element.
    """
    return SPACE.join([name for name in names if isinstance(name, str)])


def render_html_style(style: Mapping[str, Any]) -> str:
    """
    Renders the inline style of an HTML element.
    """
    return SEMICOLON.join([COLON.join([snake_to_kebab(k), v]) for k, v in style.items()])


def element(callback: Callable[..., Renderable]) -> Callable[..., str]:
    """
    A decorator for defining functional elements.
    """
    @wraps(callback)
    def wrapper(**kwargs: Any) -> str:
        return render_core(callback(**kwargs))
    return wrapper


def html_element(callback: Callable[..., Renderable]) -> Callable[..., str]:
    """
    A decorator for defining functional HTML elements.
    """
    @wraps(callback)
    def wrapper(**kwargs: Any) -> str:
        return Raw(render_html(callback(**kwargs)))
    return wrapper


class Raw(str):
    pass


class Element:

    def render(self) -> Renderable:
        return None

    def __str__(self) -> str:
        return render_core(self.render())


class DocType(Element):

    def __init__(self, dtd: str | None = None) -> None:
        self.dtd = dtd

    def render(self) -> Renderable:
        def get_dtd() -> str:
            if isinstance(self.dtd, str):
                return escape_html(self.dtd)
            return 'html'

        return '<!DOCTYPE{}>'.format(SPACE + get_dtd())


class HtmlElement(Element):

    def __init__(self, tag: str | None = None, void: bool = False, children: Renderable = None, **attributes: Any) -> None:
        self.tag = tag
        self.void = void
        self.children = children
        self.attributes = attributes

    def render(self) -> Renderable:
        def get_format() -> str:
            if self.void:
                return '<{tag}{attributes}/>'
            return '<{tag}{attributes}>{children}</{tag}>'

        options = {
            'tag': self.tag,
            'children': render_html(self.children),
            'attributes': render_html_attributes(self.attributes),
        }

        return Raw(get_format().format(**options))

    def __str__(self) -> str:
        return render_html(self.render())


class Anchor(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='a', void=False)


class Abbreviation(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='abbr', void=False)


class Address(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='address', void=False)


class Area(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='area', void=True)


class Article(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='article', void=False)


class Aside(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='aside', void=False)


class Audio(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='audio', void=False)


class Bold(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='b', void=False)


class Base(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='base', void=True)


class BidirectionalIsolate(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='bdi', void=False)


class BidirectionalOverride(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='bdo', void=False)


class BlockQuote(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='blockquote', void=False)


class Body(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='body', void=False)


class Break(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='br', void=True)


class Button(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='button', void=False)


class Canvas(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='canvas', void=False)


class Caption(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='caption', void=False)


class Cite(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='cite', void=False)


class Code(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='code', void=False)


class Column(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='col', void=True)


class ColumnGroup(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='colgroup', void=False)


class Data(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='data', void=False)


class DataList(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='datalist', void=False)


class DescriptionItem(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='dd', void=False)


class Deleted(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='del', void=False)


class Details(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='details', void=False)


class Definition(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='dfn', void=False)


class Dialog(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='dialog', void=False)


class Block(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='div', void=False)


class DescriptionList(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='dl', void=False)


class DescriptionTerm(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='dt', void=False)


class Emphasis(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='em', void=False)


class Embed(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='embed', void=True)


class FieldSet(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='fieldset', void=False)


class FigureCaption(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='figcaption', void=False)


class Figure(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='figure', void=False)


class Footer(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='footer', void=False)


class Form(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='form', void=False)


class Head(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='head', void=False)


class Header(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='header', void=False)


class Heading(HtmlElement):

    def __init__(self, size: int = 1, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='h{}'.format(size))


class HeaderGroup(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='hgroup', void=False)


class Rule(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='hr', void=True)


class Html(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='html', void=False)


class Italic(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='i', void=False)


class Iframe(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='iframe', void=False)


class Image(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='img', void=True)


class Input(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='input', void=True)


class Inserted(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='ins', void=False)


class Keyboard(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='kbd', void=False)


class Label(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='label', void=False)


class Legend(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='legend', void=False)


class ListItem(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='li', void=False)


class Link(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='link', void=True)


class Main(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='main', void=False)


class Map(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='map', void=False)


class Mark(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='mark', void=False)


class Menu(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='menu', void=False)


class Meta(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='meta', void=True)


class Meter(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='meter', void=False)


class Navigation(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='nav', void=False)


class NoScript(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='noscript', void=False)


class Object(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='object', void=False)


class OrderedList(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='ol', void=False)


class OptionGroup(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='optgroup', void=False)


class Option(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='option', void=False)


class Output(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='output', void=False)


class Paragraph(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='p', void=False)


class Parameter(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='param', void=True)


class Picture(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='picture', void=False)


class Preformatted(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='pre', void=False)


class Progress(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='progress', void=False)


class Quote(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='q', void=False)


class RubyBase(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='rb', void=False)


class RubyParenthesis(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='rp', void=False)


class RubyText(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='rt', void=False)


class RubyTextContainer(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='rtc', void=False)


class Ruby(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='ruby', void=False)


class Strikethrough(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='s', void=False)


class Sample(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='samp', void=False)


class Script(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='script', void=False)


class Section(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='section', void=False)


class Select(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='select', void=False)


class Slot(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='slot', void=False)


class Small(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='small', void=False)


class Source(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='source', void=True)


class Inline(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='span', void=False)


class Strong(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='strong', void=False)


class Style(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='style', void=False)


class Subscript(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='sub', void=False)


class Summary(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='summary', void=False)


class Superscript(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='sup', void=False)


class Table(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='table', void=False)


class TableBody(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='tbody', void=False)


class TableCell(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='td', void=False)


class Template(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='template', void=False)


class TextArea(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='textarea', void=False)


class TableFoot(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='tfoot', void=False)


class TableHeadCell(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='th', void=False)


class TableHead(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='thead', void=False)


class Time(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='time', void=False)


class Title(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='title', void=False)


class TableRow(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='tr', void=False)


class Track(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='track', void=True)


class Underline(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='u', void=False)


class UnorderedList(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='ul', void=False)


class Variable(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='var', void=False)


class Video(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='video', void=False)


class WordBreak(HtmlElement):

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs, tag='wbr', void=True)
