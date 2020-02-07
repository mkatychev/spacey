# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="spacey",
    version="0.1.0",
    description="A simple pure python library for the most common GIS functionality.",
    license="MIT",
    author="Mikhail Katychev",
    author_email="mkatych@gmail.com",
    url="https://github.com/mkatychev/spacey",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
)
