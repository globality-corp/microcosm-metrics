"""
Test decorators.

"""
from time import sleep

from hamcrest import (
    assert_that,
    empty,
    equal_to,
    greater_than,
    is_,
    not_none,
)
from microcosm.api import create_object_graph


def test_metrics_timing():
    """
    Validate that the timing decorator calls a histogram.

    """
    graph = create_object_graph("example", testing=True)
    graph.use(
        "statsd",
        "metrics_timing",
    )
    graph.lock()

    assert_that(graph.metrics_timing, is_(not_none()))

    @graph.metrics_timing("foo")
    def foo():
        sleep(1.0)

    foo()
    graph.metrics.histogram.assert_called()

    _, args, kwargs = graph.metrics.histogram.mock_calls[0]
    name, value = args

    assert_that(name, is_(equal_to("microcosm.foo")))
    assert_that(value, is_(greater_than(1.0)))
    assert_that(kwargs, is_(empty()))
