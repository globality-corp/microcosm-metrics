"""
Factories for statsd/metrics clients.

"""
from os import environ

from datadog import DogStatsd
from microcosm.api import defaults


@defaults(
    host="localhost",
    port=8125,
    tags=[],
)
def configure_datadog_statsd(graph):
    """
    Create a DataDog statsd client.

    """
    if graph.metadata.testing:
        from mock import MagicMock
        cls = MagicMock
    else:
        cls = DogStatsd

    statsd = cls(
        host=graph.config.datadog_statsd.host,
        port=graph.config.datadog_statsd.port,
        constant_tags=[
            "service:" + graph.metadata.name,
            # An empty string is *not* a valid value: tags cannot end with a colon.
            # An environment variable can be set to an empty string. We force empty strings
            # into "undefined".
            "environment:" + (environ.get("MICROCOSM_ENVIRONMENT", "") or "undefined")
        ] + graph.config.datadog_statsd.tags,
    )

    return graph.assign("metrics", statsd)
