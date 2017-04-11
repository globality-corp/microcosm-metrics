"""
Naming conventions.

"""


CALL = "call"
FAILURE = "failure"
IGNORE = "ignore"
SUCCESS = "success"


def name_for(*keys, **kwargs):
    """
    Concatenate a metric name.

    """
    prefix = kwargs.get("prefix", "microcosm")
    return ".".join([prefix] + list(keys))
