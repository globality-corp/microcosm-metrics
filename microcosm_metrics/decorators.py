"""
Metrics decorators.

"""
from functools import wraps
from os import environ
from time import time

from microcosm_metrics.classifier import Classifier
from microcosm_metrics.naming import name_for


def configure_metrics_counting(graph):
    """
    Configure a counting decorator.

    """
    def metrics_counting(name, classifier_cls=Classifier):
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
                    environment = environ.get("MICROCOSM_ENVIRONMENT", "undefined")
                    if classifier.label is not None:
                        graph.metrics.increment(
                            name_for(
                                name,
                                classifier.label,
                                "count",
                                prefix=graph.metadata.name,
                                environment=environment,
                            ),
                        )
            return wrapper
        return decorator
    return metrics_counting


def configure_metrics_timing(graph):
    """
    Configure a timing decorator.

    """
    def metrics_timing(name):
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
                    environment = environ.get("MICROCOSM_ENVIRONMENT", "undefined")
                    graph.metrics.histogram(
                        name_for(
                            name,
                            prefix=graph.metadata.name,
                            environment=environment,
                        ),
                        end_time - start_time,
                    )
            return wrapper
        return decorator
    return metrics_timing
