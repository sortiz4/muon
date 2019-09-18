from muon import Body
from muon import DocType
from muon import Element
from muon import Head
from muon import Heading
from muon import Html
from muon import Input
from muon import Link
from muon import Raw
from muon import Script
from muon import Title


class Document(Element):

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


class Test(Element):

    def render(self):
        return Document(
            head=[
                Link(rel='stylesheet', href='index.scss'),
                Script(src='index.js'),
                Title(children='Test'),
            ],
            body=[
                Heading(children='This is a test!'),
                Input(
                    style={
                        'font_family': 'Courier',
                        'font_size': '20px',
                    },
                    readonly=True,
                    required=False,
                ),
                Raw('</BAD"\'>'),
                '</BAD"\'>',
            ],
        )


if __name__ == '__main__':
    print(Test())
