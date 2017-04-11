"""
Naming tests.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from microcosm_metrics.naming import name_for


def test_naming():
    assert_that(name_for("foo", "bar"), is_(equal_to("microcosm.foo.bar")))


def test_naming_prefix():
    assert_that(name_for("foo", prefix="example"), is_(equal_to("example.foo")))
