"""
Test result classification.

"""
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_,
    none,
    raises,
)

from microcosm_metrics.classifier import Classifier, FailOnErrorClassifier
from microcosm_metrics.naming import CALL, FAILURE, SUCCESS


def test_classifier_returning_result():

    def func():
        return

    classifier = Classifier(func)
    assert_that(classifier.label, is_(none()))
    classifier()
    assert_that(classifier.label, is_(equal_to(CALL)))


def test_classifier_raising_error():

    def func():
        raise Exception

    classifier = Classifier(func)
    assert_that(classifier.label, is_(none()))
    assert_that(calling(classifier), raises(Exception))
    assert_that(classifier.label, is_(equal_to(CALL)))


def test_fail_on_error_returning_result():

    def func():
        return

    classifier = FailOnErrorClassifier(func)
    assert_that(classifier.label, is_(none()))
    classifier()
    assert_that(classifier.label, is_(equal_to(SUCCESS)))


def test_fail_on_error_raising_error():

    def func():
        raise Exception

    classifier = FailOnErrorClassifier(func)
    assert_that(classifier.label, is_(none()))
    assert_that(calling(classifier), raises(Exception))
    assert_that(classifier.label, is_(equal_to(FAILURE)))
