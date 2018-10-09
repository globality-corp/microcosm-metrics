#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-metrics"
version = "2.1.0"

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
        "datadog>=0.17.0",
        "microcosm>=2.0.0",
        "microcosm-logging>=1.0.0",
        "pyopenssl>=0.14",
    ],
    setup_requires=[
        "nose>=1.3.6",
    ],
    dependency_links=[
    ],
    entry_points={
        "console_scripts": [
            "publish-metric = microcosm_metrics.main:publish",
        ],
        "microcosm.factories": [
            "datadog_statsd = microcosm_metrics.factories:configure_datadog_statsd",
            "metrics = microcosm_metrics.factories:configure_metrics",
            "metrics_counting = microcosm_metrics.decorators:configure_metrics_counting",
            "metrics_timing = microcosm_metrics.decorators:configure_metrics_timing",
        ],
    },
    tests_require=[
        "coverage>=3.7.1",
        "mock>=2.0.0",
        "PyHamcrest>=1.9.0",
    ],
)
