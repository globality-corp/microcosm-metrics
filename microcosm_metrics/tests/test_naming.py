"""
Naming tests.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from microcosm_metrics.naming import name_for


class TestNaming:

    def test_naming(self):
        assert_that(name_for("foo", "bar"), is_(equal_to("foo.bar")))

    def test_naming_simple(self):
        assert_that(name_for("foo"), is_(equal_to("foo")))
