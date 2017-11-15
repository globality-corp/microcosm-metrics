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
    environment = kwargs.get("environment", "undefined")
    return ".".join([environment, prefix] + list(keys))
