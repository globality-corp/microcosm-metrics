"""
Factories for statsd/metrics clients.

"""
from types import MethodType

from datadog import DogStatsd
from microcosm.api import defaults
from statsd import StatsClient


def attach(graph, statsd):
    """
    Attach statsd client to `metrics` key for pseudo polymorphism.

    """
    return graph.assign("metrics", statsd)


@defaults(
    host="localhost",
    port=8125,
    tags=[],
)
def configure_statsd(graph):
    """
    Create a vanilla statsd client.

    """
    if graph.metadata.testing:
        from mock import MagicMock
        cls = MagicMock
    else:
        cls = StatsClient

    statsd = cls(
        host=graph.config.datadog_statsd.host,
        port=graph.config.datadog_statsd.port,
    )

    if not graph.metadata.testing:
        # We have different interfaces between the StatsClient and DogStatsd. Try to adapt the
        # former to the latter for the decorator use cases.
        def histogram(self, stat, value, rate=1):
            return self._send_stat(stat, "{}|h".format(value), rate)

        statsd.increment = statsd.incr
        statsd.histogram = MethodType(histogram, statsd)

    return attach(graph, statsd)


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
            graph.metadata.name,
        ] + graph.config.datadog_statsd.tags,
    )

    return attach(graph, statsd)
