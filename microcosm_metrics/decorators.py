"""
Metrics decorators.

"""
from functools import wraps
from time import time

from microcosm_metrics.classifier import Classifier
from microcosm_metrics.naming import name_for


def configure_metrics_counting(graph):
    """
    Configure a counting decorator.

    """
    graph.use("metrics")

    def metrics_counting(name, tags=None, classifier_cls=Classifier):
        """
        Create a decorator that counts a specific context.

        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                classifier = classifier_cls(func)
                try:
                    return classifier(*args, **kwargs)
                finally:
                    if classifier.label is not None:
                        graph.metrics.increment(
                            name_for(
                                name,
                                classifier.label,
                                "count",
                            ),
                            tags=tags,
                        )
            return wrapper
        return decorator
    return metrics_counting


def configure_metrics_timing(graph):
    """
    Configure a timing decorator.

    """
    graph.use("metrics")

    def metrics_timing(name, tags=None):
        """
        Create a decorator that times a specific context.

        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time()
                try:
                    return func(*args, **kwargs)
                finally:
                    end_time = time()
                    graph.metrics.histogram(
                        name_for(name),
                        end_time - start_time,
                        tags=tags,
                    )
            return wrapper
        return decorator
    return metrics_timing
