# !/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    with open(filename) as f:
        raw_text = f.read()
        required_libraries = [
            line
            for line in raw_text.splitlines()
            if (not line.startswith("#")) and (not line.startswith("-"))
        ]
    return required_libraries


setup(
    name="wemmick",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    version="0.0.1",
    description="A Great Expectations bundle for BERA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BERA",
    url="https://github.com/BERA/wemmick",
    install_requires=parse_requirements("requirements-base.txt"),
    entry_points={"console_scripts": ["wemmick=wemmick.cli:app"]},
    include_package_data=True,
)
