"""
Naming conventions.

"""


CALL = "call"
FAILURE = "failure"
IGNORE = "ignore"
SUCCESS = "success"


def name_for(*keys):
    """
    Concatenate a metric name.

    """
    return ".".join(keys)
