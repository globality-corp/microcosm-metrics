"""
Test decorators.

"""
from collections import OrderedDict
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


def test_metrics_counting():
    """
    Validate that the counting decorator calls increment.

    """
    graph = create_object_graph("example", testing=True)
    graph.use(
        "statsd",
        "metrics_counting",
    )
    graph.lock()

    assert_that(graph.metrics_counting, is_(not_none()))

    @graph.metrics_counting("foo")
    def foo():
        pass

    foo()
    graph.metrics.increment.assert_called()

    _, args, kwargs = graph.metrics.increment.mock_calls[0]
    name, = args

    assert_that(name, is_(equal_to("example.foo.call.count")))
    assert_that(kwargs, is_(empty()))


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

    assert_that(name, is_(equal_to("example.foo")))
    assert_that(value, is_(greater_than(1.0)))
    assert_that(kwargs, is_(empty()))


def test_metrics_timing_with_tags():
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

    @graph.metrics_timing("foo", OrderedDict(
        same=None,
        same_none=None,
        prefix=lambda x: '-' + x,
        prefix_none=lambda x: '-' + x))
    def foo(**kwargs):
        sleep(1.0)

    foo(same="same", prefix="prefix")
    graph.metrics.histogram.assert_called()

    _, args, kwargs = graph.metrics.histogram.mock_calls[0]
    name, value = args

    assert_that(name, is_(equal_to("example.foo")))
    assert_that(value, is_(greater_than(1.0)))
    assert_that(kwargs, is_(equal_to(dict(tags=["same", "-prefix"]))))
