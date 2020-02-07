# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = (
        "A simple pure python library for the most common GIS functionality."
    )

setup(
    name="spacey",
    version="0.1.1",
    description="A simple pure python library for the most common GIS functionality.",
    license="MIT",
    author="Mikhail Katychev",
    author_email="mkatych@gmail.com",
    url="https://github.com/mkatychev/spacey",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
)
