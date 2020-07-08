# !/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# Parse requirements.txt
with open("requirements-base.txt") as f:
    raw_text = f.read()
    required_libraries = [
        line
        for line in raw_text.splitlines()
        if (not line.startswith("#")) and (not line.startswith("-"))
    ]

with open("requirements-http.txt") as f:
    raw_text = f.read()
    required_libraries.append([
        line
        for line in raw_text.splitlines()
        if (not line.startswith("#")) and (not line.startswith("-"))
    ])

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
    install_requires=required_libraries,
    entry_points={"console_scripts": ["wemmick=wemmick.cli:app"]},
    include_package_data=True,
)
