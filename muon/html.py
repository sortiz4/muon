from muon.core import HtmlElement

TAGS = (
    'a',
    'abbr',
    'address',
    'area',
    'article',
    'aside',
    'audio',
    'b',
    'base',
    'bdi',
    'bdo',
    'blockquote',
    'body',
    'br',
    'button',
    'canvas',
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'data',
    'datalist',
    'dd',
    'del',
    'details',
    'dfn',
    'dialog',
    'div',
    'dl',
    'dt',
    'em',
    'embed',
    'fieldset',
    'figcaption',
    'figure',
    'footer',
    'form',
    'head',
    'header',
    'hgroup',
    'hr',
    'html',
    'i',
    'iframe',
    'img',
    'input',
    'ins',
    'kbd',
    'label',
    'legend',
    'li',
    'link',
    'main',
    'map',
    'mark',
    'menu',
    'meta',
    'meter',
    'nav',
    'noscript',
    'object',
    'ol',
    'optgroup',
    'option',
    'output',
    'p',
    'param',
    'picture',
    'pre',
    'progress',
    'q',
    'rb',
    'rp',
    'rt',
    'rtc',
    'ruby',
    's',
    'samp',
    'section',
    'select',
    'slot',
    'small',
    'source',
    'span',
    'strong',
    'style',
    'sub',
    'summary',
    'sup',
    'table',
    'tbody',
    'td',
    'template',
    'tfoot',
    'th',
    'thead',
    'time',
    'title',
    'tr',
    'track',
    'u',
    'ul',
    'var',
    'video',
    'wbr',
)


def _types():
    """
    """
    def _methods(tag):
        """
        """
        def __init__(self, **kwargs):
            HtmlElement.__init__(self, **kwargs, tag=tag)

        #
        return {'__init__': __init__}

    #
    types = {}
    for tag in TAGS:
        name = tag.capitalize()
        types[name] = type(name, (HtmlElement,), _methods(tag))
    return types


class H(HtmlElement):

    def __init__(self, size=1, **kwargs):
        super().__init__(**kwargs, tag='h{}'.format(size))


class Script(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='script')
        self.FORMAT_A = self.FORMAT_B


class Textarea(HtmlElement):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, tag='textarea')
        self.FORMAT_A = self.FORMAT_B


globals().update(_types())
