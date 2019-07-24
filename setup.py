#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""


from setuptools import setup, find_packages


requirements = ["Click>=6.0", "pandas", "requests"]
setup_requirements = ["pytest-runner"]
test_requirements = ["pytest", "coverage"]

setup(
    author="Vaastav Anand",
    author_email="",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="",
    entry_points={"console_scripts": ["fpl=fpl_tools.cli:main"]},
    install_requires=requirements,
    license="MIT License",
    long_description="",
    include_package_data=True,
    keywords="fpl premierleague fantasypremierleague",
    name="fpl_tools",
    packages=find_packages(include=["fpl_tools"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/vaastav/Fantasy-Premier-League",
    version="0.1.1",
    zip_safe=False,
)
