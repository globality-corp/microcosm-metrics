"""
Factories for statsd/metrics clients.

"""
from os import environ
from warnings import warn

from datadog import DogStatsd
from microcosm.api import defaults


@defaults(
    host="localhost",
    port=8125,
    tags=[],
)
def configure_datadog_statsd(graph):
    """
    Deprecated: use `configure_metrics`
    """
    warn(
        "Deprecated: use configure_metrics instead",
        DeprecationWarning,
    )

    metrics = configure_metrics(graph, 'datadog_statsd')
    return graph.assign("metrics", metrics)


@defaults(
    host="localhost",
    port=8125,
    tags=[],
)
def configure_metrics(graph, configuration='metrics'):
    """
    Create a DataDog-extension-based statsd client.
    """
    if graph.metadata.testing:
        from mock import MagicMock
        cls = MagicMock
    else:
        cls = DogStatsd

    config = getattr(graph.config, configuration)

    statsd = cls(
        host=config.host,
        port=config.port,
        constant_tags=[
            "service:" + graph.metadata.name,
            # An empty string is *not* a valid value: tags cannot end with a colon.
            # An environment variable can be set to an empty string. We force empty strings
            # into "undefined".
            "environment:" + (environ.get("MICROCOSM_ENVIRONMENT", "") or "undefined")
        ] + config.tags,
    )

    return statsd
