import io
import os
import re

from setuptools import find_packages, setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(
            text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read()
        )


setup(
    name="common_utils",
    version="0.0.1",
    url="https://github.com/pollitosabroson/test-common_utils",
    license="MIT",
    author="Alejandro hernandez",
    author_email="alejandro.hernandez@neutroon.com",
    description="Functionalities that are common within our projects",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("tests",)),
    install_requires=["ariadne==0.15.0", "ipython==7.31.0"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
