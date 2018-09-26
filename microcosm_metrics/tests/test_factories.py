"""
Factory tests.

"""
from hamcrest import (
    assert_that,
    contains,
    equal_to,
    is_,
    not_none,
)
from microcosm.api import create_object_graph


def test_datadog_statsd():
    """
    Assert that factory returns something.

    Note that during unit tests, the result will be a MagicMock.

    """
    graph = create_object_graph("example", testing=True)
    graph.use("datadog_statsd")
    graph.lock()

    assert_that(graph.datadog_statsd, is_(not_none()))
    assert_that(graph.metrics, is_(not_none()))

    assert_that(graph.metrics.host, is_(equal_to("localhost")))
    assert_that(graph.metrics.port, is_(equal_to(8125)))
    assert_that(graph.metrics.constant_tags, contains("service:example", "environment:undefined"))
