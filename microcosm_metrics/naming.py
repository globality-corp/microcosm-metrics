"""
Naming conventions.

"""


CALL = "call"
FAILURE = "failure"
IGNORE = "ignore"
SUCCESS = "success"


def name_for(*keys, prefix="microcosm"):
    """
    Concatenate a metric name.

    """
    return ".".join([prefix] + list(keys))
