# !/usr/bin/env python

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Parse requirements.txt
with open("requirements.txt") as f:
    raw_text = f.read()
    required_libraries = [
        line
        for line in raw_text.splitlines()
        if (not line.startswith("#")) and (not line.startswith("-"))
    ]
    print(required_libraries)

setup(
    name="dataquality",
    packages=["dataquality"],
    version="0.0.1",
    description="Data quality library for Great Expectations extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BERA",
    url="https://github.com/BERA/sdap",
    install_requires=required_libraries,
    entry_points={"console_scripts": ["dataquality=dataquality.cli:app"]},
    include_package_data=True,
)
