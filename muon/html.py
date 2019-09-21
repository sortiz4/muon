from muon.core import HtmlElement

__all__ = [
    'Heading',
    'Script',
    'TextArea',
]

TAGS = (
    ('a', 'Anchor'),
    ('abbr', 'Abbreviation'),
    ('address', None),
    ('area', None),
    ('article', None),
    ('aside', None),
    ('audio', None),
    ('b', 'Bold'),
    ('base', None),
    ('bdi', 'BidirectionalIsolate'),
    ('bdo', 'BidirectionalOverride'),
    ('blockquote', 'BlockQuote'),
    ('body', None),
    ('br', 'Break'),
    ('button', None),
    ('canvas', None),
    ('caption', None),
    ('cite', None),
    ('code', None),
    ('col', 'Column'),
    ('colgroup', 'ColumnGroup'),
    ('data', None),
    ('datalist', 'DataList'),
    ('dd', 'DescriptionItem'),
    ('del', 'Deleted'),
    ('details', None),
    ('dfn', 'Definition'),
    ('dialog', None),
    ('div', 'Block'),
    ('dl', 'DescriptionList'),
    ('dt', 'DescriptionTerm'),
    ('em', 'Emphasis'),
    ('embed', None),
    ('fieldset', 'FieldSet'),
    ('figcaption', 'FigureCaption'),
    ('figure', None),
    ('footer', None),
    ('form', None),
    ('head', None),
    ('header', None),
    ('hgroup', 'HeaderGroup'),
    ('hr', 'Rule'),
    ('html', None),
    ('i', 'Italic'),
    ('iframe', None),
    ('img', 'Image'),
    ('input', None),
    ('ins', 'Inserted'),
    ('kbd', 'Keyboard'),
    ('label', None),
    ('legend', None),
    ('li', 'ListItem'),
    ('link', None),
    ('main', None),
    ('map', None),
    ('mark', None),
    ('menu', None),
    ('meta', None),
    ('meter', None),
    ('nav', 'Navigation'),
    ('noscript', 'NoScript'),
    ('object', None),
    ('ol', 'OrderedList'),
    ('optgroup', 'OptionGroup'),
    ('option', None),
    ('output', None),
    ('p', 'Paragraph'),
    ('param', 'Parameter'),
    ('picture', None),
    ('pre', 'Preformatted'),
    ('progress', None),
    ('q', 'Quote'),
    ('rb', 'RubyBase'),
    ('rp', 'RubyParenthesis'),
    ('rt', 'RubyText'),
    ('rtc', 'RubyTextContainer'),
    ('ruby', None),
    ('s', 'Strikethrough'),
    ('samp', 'Sample'),
    ('section', None),
    ('select', None),
    ('slot', None),
    ('small', None),
    ('source', None),
    ('span', 'Inline'),
    ('strong', None),
    ('style', None),
    ('sub', 'Subscript'),
    ('summary', None),
    ('sup', 'Superscript'),
    ('table', None),
    ('tbody', 'TableBody'),
    ('td', 'TableCell'),
    ('template', None),
    ('tfoot', 'TableFooter'),
    ('th', 'TableHeaderCell'),
    ('thead', 'TableHeader'),
    ('time', None),
    ('title', None),
    ('tr', 'TableRow'),
    ('track', None),
    ('u', 'Underline'),
    ('ul', 'UnorderedList'),
    ('var', 'Variable'),
    ('video', None),
    ('wbr', 'WordBreak'),
)


def _types():
    """
    """
    global __all__

    def _methods(tag):
        """
        """
        def __init__(self, **kwargs):
            HtmlElement.__init__(self, **kwargs, tag=tag)

        #
        return {'__init__': __init__}

    #
    types = {}
    for tag, name in TAGS:
        if name is None:
            name = tag.capitalize()
        types[name] = type(name, (HtmlElement,), _methods(tag))
    
    #
    __all__ += [*types.keys()]

    #
    return types


class Heading(HtmlElement):

    def __init__(self, size=1, **kwargs):
        super().__init__(**kwargs, tag='h{}'.format(size))


class Script(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='script')
        self.FORMAT_A = self.FORMAT_B


class TextArea(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='textarea')
        self.FORMAT_A = self.FORMAT_B


globals().update(_types())
