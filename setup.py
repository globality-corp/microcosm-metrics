#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-metrics"
version = "0.1.0"

setup(
    name=project,
    version=version,
    description="Opinionated metrics configuration",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/microcosm-metrics",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    keywords="microcosm",
    install_requires=[
        "microcosm>=0.16.0",
        "microcosm-logging>=0.13.0",
    ],
    setup_requires=[
        "nose>=1.3.6",
    ],
    dependency_links=[
    ],
    entry_points={
        "microcosm.factories": [
        ],
    },
    tests_require=[
        "coverage>=3.7.1",
        "mock>=2.0.0",
        "PyHamcrest>=1.9.0",
    ],
)
