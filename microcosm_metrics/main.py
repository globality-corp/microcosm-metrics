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
    parser.add_argument("--action", choices=["increment", "histogram"], default="increment")
    return parser.parse_args()


def create_statsd_client(args):
    loader = load_from_dict(dict(
        metrics=dict(
            host=args.host,
        ),
    ))
    graph = create_object_graph("example", loader=loader)
    graph.use("metrics")
    graph.lock()

    return graph.metrics


def publish():
    """
    Publish a metric (for testing).

    """
    args = parse_args()
    statsd = create_statsd_client(args)

    if args.action == "increment":
        statsd.increment(name_for(getuser(), args.action))
    elif args.action == "histogram":
        statsd.histogram(name_for(getuser(), args.action), 1.0)

    try:
        # wait a little to allow the delivery of the metric before we exit
        sleep(1.0)
    except KeyboardInterrupt:
        pass
