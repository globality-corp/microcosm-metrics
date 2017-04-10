"""
Test CLI for metric integration.

"""
from argparse import ArgumentParser
from getpass import getuser
from time import sleep

from microcosm.api import create_object_graph
from microcosm.loaders import load_from_dict

from microcosm_metrics.naming import name_for


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--host", default="localhost")
    return parser.parse_args()


def create_statsd_client():
    args = parse_args()
    loader = load_from_dict(dict(
        datadog_statsd=dict(
            host=args.host,
        ),
    ))
    graph = create_object_graph("metrics", loader=loader)
    graph.use("datadog_statsd")
    graph.lock()

    return graph.metrics


def publish():
    """
    Publish a metric (for testing).

    """
    statsd = create_statsd_client()

    statsd.increment(name_for(getuser()))

    try:
        # wait a little to allow the delivery of the metric before we exit
        sleep(1.0)
    except KeyboardInterrupt:
        pass
