"""
Label function outcomes.

"""
from functools import wraps

from microcosm_metrics.naming import CALL, FAILURE, SUCCESS


class Classifier:
    """
    A classifier produces labels based on the outcomes of a wrapped function.

    By default, every outcome is labeled "call"

    Subclasses can specialize this behavior.

    """
    def __init__(self, func):
        self.label = None
        self.func = func
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        """
        Call the wrapped function and classify the result.

        """
        try:
            result = self.func(*args, **kwargs)
            self.label = self.label_result(result)
            return result
        except Exception as error:
            self.label = self.label_error(error)
            raise

    def label_result(self, result):
        return CALL

    def label_error(self, error):
        return CALL


class FailOnErrorClassifier(Classifier):
    """
    A classifier that counts errors as failures.

    """
    def label_result(self, result):
        return SUCCESS

    def label_error(self, error):
        return FAILURE
