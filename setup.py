# coding: utf-8

from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "entitygraph"
VERSION = "0.0.1"
PYTHON_REQUIRES = ">=3.7"
REQUIRES = [
    "requests >= 2.31.0",
    "python-dateutil",
    "pydantic >= 1.10.5, < 2",
    "aenum"
]

setup(
    name=NAME,
    version=VERSION,
    description="Python client for Maverick EntityGraph API",
    author="Bechtle A/V Software Solutions 360°",
    author_email="mail@a365maverick.de",
    url="",
    keywords=["Maverick", "EntityGraph", "API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache 2.0",
    long_description_content_type='text/markdown',
    package_data={"entitygraph": ["py.typed"]},
)
