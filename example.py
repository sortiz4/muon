from muon import Body
from muon import DocType
from muon import Head
from muon import Heading
from muon import Html
from muon import html_element
from muon import HtmlElement
from muon import Input
from muon import Link
from muon import Meta
from muon import Raw
from muon import Script
from muon import Title


def document(head, body):
    return [
        DocType(),
        Html(
            lang='en',
            children=[
                Head(children=head),
                Body(children=body),
            ],
        ),
    ]


def example(element):
    return element(
        head=[
            Meta(charset='utf-8'),
            Meta(http_equiv='x-ua-compatible', content='ie=edge'),
            Meta(name='viewport', content='width=device-width, initial-scale=1'),
            Link(href='/static/favicon.png', rel='icon', type='image/png'),
            Script(src='/static/index.js', type='application/javascript', defer=True),
            Title(children='Example'),
        ],
        body=[
            Heading(
                classname='heading large',
                children='This is a heading',
            ),
            Input(
                classname=[
                    'input',
                    'large',
                ],
                style={
                    'font_family': 'Courier',
                    'font_size': '20px',
                },
                value='This is a value',
                maxlength=30,
                readonly=False,
                required=True,
            ),
            Raw('\'"><'),
            '\'"><',
        ],
    )


class Document1(HtmlElement):

    def __init__(self, head=None, body=None):
        self.head = head
        self.body = body

    def render(self):
        return document(self.head, self.body)


class Example1(HtmlElement):

    def render(self):
        return example(Document1)


@html_element
def Document2(head=None, body=None):
    return document(head, body)


@html_element
def Example2():
    return example(Document2)


if __name__ == '__main__':
    print(Example1())
    print(Example2())
