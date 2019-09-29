from muon import Body
from muon import DocType
from muon import Head
from muon import Heading
from muon import Html
from muon import html_element
from muon import HtmlElement
from muon import Input
from muon import Link
from muon import Raw
from muon import Script
from muon import Title


def document(head, body):
    return [
        DocType(),
        Html(
            children=[
                Head(children=head),
                Body(children=body),
            ],
        ),
    ]


def test(element):
    return element(
        head=[
            Link(rel='stylesheet', href='index.scss'),
            Script(src='index.js'),
            Title(children='Test'),
        ],
        body=[
            Heading(
                classname='heading large',
                children='This is a test!',
            ),
            Input(
                classname=[
                    'input',
                    'large',
                    'simple',
                ],
                maxlength=30,
                readonly=False,
                required=True,
                style={
                    'font_family': 'Courier',
                    'font_size': '20px',
                },
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


class Test1(HtmlElement):

    def render(self):
        return test(Document1)


@html_element
def Document2(head=None, body=None):
    return document(head, body)


@html_element
def Test2():
    return test(Document2)


if __name__ == '__main__':
    print(Test1())
    print(Test2())
