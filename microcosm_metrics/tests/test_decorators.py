"""
Test decorators.

"""
from os import environ
from time import sleep

from hamcrest import (
    assert_that,
    close_to,
    empty,
    equal_to,
    is_,
    none,
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
            "metrics",
            "metrics_counting",
        )
        graph.lock()

        assert_that(graph.metrics_counting, is_(not_none()))

        @graph.metrics_counting("foo")
        def foo():
            pass

        foo()
        foo()
        graph.metrics.increment.assert_called()
        assert_that(graph.metrics.increment.call_count, is_(2))

        for call in graph.metrics.increment.mock_calls:
            _, args, kwargs = call
            name, = args

            assert_that(name, is_(equal_to("foo.call.count")))
            assert_that(kwargs.pop("tags", None), is_(equal_to(['classifier:call'])))
            assert_that(kwargs, is_(empty()))

    def test_metrics_timing(self):
        """
        Validate that the timing decorator calls a histogram.

        """
        graph = create_object_graph("example", testing=True)
        graph.use(
            "metrics",
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
        assert_that(value, is_(close_to(1000, 100)))
        assert_that(kwargs.pop("tags", None), is_(none()))
        assert_that(kwargs, is_(empty()))
