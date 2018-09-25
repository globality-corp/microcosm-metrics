# microcosm-metrics

Opinionated metrics configuration.

Designed to support [DataDog statsd](http://docs.datadoghq.com/guides/dogstatsd/)-compatible servers.

## Usage

 1. Configure a metrics client:

        graph.use("datadog_statsd")

 2. Use the resulting `graph.metrics` client:

        graph.metrics.increment("foo")


## Decorators

The two most common metrics usages are supported via decorator interfaces.

To time function calls, use:

    @graph.metrics_timing("my_func")
    def my_func():
        pass

To count function outcomes, use:

    @graph.metrics_counting("my_func")
    def my_func():
        pass

For counting, the default behavior is to count function *calls*. To count different outcomes,
use a custom `Classifier`:

    class TruthyClassifier(Classifier):

        def label_result(self, result):
            return "truthy" if bool(result) else "falsey"

        def label_error(self, error):
            return None

Then pass the classifier class to the counting decorator:

    @graph.metrics_counting("my_func", classifier=TruthyClassifier)
    def my_func():
        pass


## StatsD Testing

First, run the `statsd` server. For example, using Docker:

    docker run --name statsd -d \
               -p 0.0.0.0:9102:9102 \
               -p 0.0.0.0:8125:9125/udp \
               prom/statsd-exporter

Then, use the included CLIT to validate connectivity:

    publish-metric --host $(docker-machine ip default)

The resulting metric should appear in the `/metrics` endpoint.

## DataDog Testing

First, run the `DataDog Agent` (requires an `API_KEY`). For example, using Docker:

    docker run -d --name datadog-agent -p 8125:8125/udp -e API_KEY=${API_KEY} datadog/docker-dd-agent:latest

Then, use the included CLI to validate connectivity:

    publish-metric --host $(docker-machine ip default)

The resulting metric should appear in `DataDog` "Metric Summary" right away.
