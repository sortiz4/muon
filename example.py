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
from muon import Renderable
from muon import Safe
from muon import Script
from muon import Title
from typing import Callable


def document(head: Renderable, body: Renderable) -> Renderable:
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


def example(element: Callable[..., Renderable]) -> Renderable:
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
                classes='heading',
                children='This is a heading',
            ),
            Input(
                classes=[
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
            Safe('\'"><'),
            '\'"><',
        ],
    )


class Document1(HtmlElement):

    def __init__(self, head: Renderable = None, body: Renderable = None) -> None:
        self.head = head
        self.body = body

    def render(self) -> Renderable:
        return document(self.head, self.body)


class Example1(HtmlElement):

    def render(self) -> Renderable:
        return example(Document1)


@html_element
def Document2(head: Renderable = None, body: Renderable = None) -> Renderable:
    return document(head, body)


@html_element
def Example2() -> Renderable:
    return example(Document2)


if __name__ == '__main__':
    print(Example1())
    print(Example2())
