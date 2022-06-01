#!/usr/bin/env python
from setuptools import setup

setup(
    name='muon',
    version='0.2',
    description='A text generation framework.',
    author='Steven Ortiz',
    url='https://github.com/sortiz4/muon',
    packages=[
        'muon',
        'muon.core',
        'muon.shortcuts',
    ],
)
