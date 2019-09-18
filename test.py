from muon import Body
from muon import DocType
from muon import Head
from muon import Heading
from muon import Html
from muon import HtmlElement
from muon import Input
from muon import Link
from muon import Raw
from muon import Script
from muon import Title


class Document(HtmlElement):

    def __init__(self, head=None, body=None):
        self.head = head
        self.body = body

    def render(self):
        return [
            DocType(),
            Html(
                children=[
                    Head(children=self.head),
                    Body(children=self.body),
                ],
            ),
        ]


class Test(HtmlElement):

    def render(self):
        return Document(
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


if __name__ == '__main__':
    print(Test())
