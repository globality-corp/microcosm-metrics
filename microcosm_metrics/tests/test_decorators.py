"""
Test decorators.

"""
from os import environ
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


class TestDecorators:

    def setup(self):
        environ["MICROCOSM_ENVIRONMENT"] = "testing"

    def teardown(self):
        environ["MICROCOSM_ENVIRONMENT"] = ""

    def test_metrics_counting(self):
        """
        Validate that the counting decorator calls increment.

        """
        graph = create_object_graph("example", testing=True)
        graph.use(
            "datadog_statsd",
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

        assert_that(name, is_(equal_to("foo.call.count")))
        assert_that(kwargs.pop("tags", None), is_(None))
        assert_that(kwargs, is_(empty()))

    def test_metrics_timing(self):
        """
        Validate that the timing decorator calls a histogram.

        """
        graph = create_object_graph("example", testing=True)
        graph.use(
            "datadog_statsd",
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

        assert_that(name, is_(equal_to("foo")))
        assert_that(value, is_(greater_than(1.0)))
        assert_that(kwargs.pop("tags", None), is_(None))
        assert_that(kwargs, is_(empty()))
