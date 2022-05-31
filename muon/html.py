from muon.core import HtmlElement

__all__ = [
    'Heading',
]


def _add_html_elements(*tags):
    """
    Adds basic HTML element types to this module.
    """
    global __all__

    def create_methods(tag, void):
        """
        Creates a map of methods for a given tag.
        """
        def __init__(self, **kwargs):
            HtmlElement.__init__(self, **kwargs, tag=tag, void=void)
        return {'__init__': __init__}

    # Construct the types
    types = {}
    for tag, name, void in tags:
        if name is None:
            name = tag.capitalize()
        types[name] = type(name, (HtmlElement,), create_methods(tag, void))

    # Augment the exports
    __all__ += [*types.keys()]

    # Update the module
    globals().update(types)


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
