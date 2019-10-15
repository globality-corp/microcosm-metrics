"""
Factories for statsd/metrics clients.

"""
from os import environ
from unittest.mock import MagicMock

from datadog import DogStatsd
from microcosm.api import defaults


@defaults(
    host="localhost",
    port=8125,
    tags=[],
)
def configure_metrics(graph, configuration="metrics"):
    """
    Create a DataDog-extension-based statsd client.
    """
    if graph.metadata.testing:
        cls = MagicMock
    else:
        cls = DogStatsd

    config = getattr(graph.config, configuration)
    metric_service_name = environ.get("METRICS_NAME", graph.metadata.name)

    statsd = cls(
        host=config.host,
        port=config.port,
        constant_tags=[
            f"service:{metric_service_name}"
            # An empty string is *not* a valid value: tags cannot end with a colon.
            # An environment variable can be set to an empty string. We force empty strings
            # into "undefined".
            "environment:" + (environ.get("MICROCOSM_ENVIRONMENT", "") or "undefined")
        ] + config.tags,
    )

    return statsd
