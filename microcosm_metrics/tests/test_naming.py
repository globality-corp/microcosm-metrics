"""
Naming tests.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)

from microcosm_metrics.naming import name_for


class TestNaming(object):

    def test_naming(self):
        assert_that(name_for("foo", "bar", environment="testing"), is_(equal_to("microcosm.testing.foo.bar")))

    def test_naming_prefix(self):
        assert_that(name_for("foo", prefix="example", environment="testing"), is_(equal_to("example.testing.foo")))
