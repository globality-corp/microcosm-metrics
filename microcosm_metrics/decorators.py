"""
Metrics decorators.

"""
from functools import wraps
from time import time

from microcosm_metrics.naming import name_for


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
                    # NB: the statsd client doesn't actually have this interface
                    graph.metrics.histogram(
                        name_for(name),
                        end_time - start_time,
                    )
            return wrapper
        return decorator
    return metrics_timing
