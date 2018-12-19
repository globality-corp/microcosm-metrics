#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-metrics"
version = "2.2.0"

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
    python_requires=">=3.6",
    keywords="microcosm",
    install_requires=[
        "datadog>=0.26.0",
        "microcosm>=2.4.1",
        "microcosm-logging>=1.3.0",
        "pyopenssl>=18.0.0",
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    dependency_links=[
    ],
    entry_points={
        "console_scripts": [
            "publish-metric = microcosm_metrics.main:publish",
        ],
        "microcosm.factories": [
            "metrics = microcosm_metrics.factories:configure_metrics",
            "metrics_counting = microcosm_metrics.decorators:configure_metrics_counting",
            "metrics_timing = microcosm_metrics.decorators:configure_metrics_timing",
        ],
    },
    tests_require=[
        "coverage>=3.7.1",
        "PyHamcrest>=1.9.0",
    ],
)
