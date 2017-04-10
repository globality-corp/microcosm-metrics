"""
Naming tests.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from microcosm_metrics.naming import name_for


def test_metrics_timing():
    assert_that(name_for("foo"), is_(equal_to("microcosm.foo")))
