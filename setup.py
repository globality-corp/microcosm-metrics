#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-metrics"
version = "0.2.3"

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
        "datadog>=0.15.0",
        "microcosm>=0.17.2",
        "microcosm-logging>=0.13.0",
        "statsd>=3.2.1",
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
            "metrics_counting = microcosm_metrics.decorators:configure_metrics_counting",
            "metrics_timing = microcosm_metrics.decorators:configure_metrics_timing",
            "statsd = microcosm_metrics.factories:configure_statsd",
        ],
    },
    tests_require=[
        "coverage>=3.7.1",
        "mock>=2.0.0",
        "PyHamcrest>=1.9.0",
    ],
)
