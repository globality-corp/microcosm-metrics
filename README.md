# microcosm-metrics

Opinionated metrics configuration.

Designed to support both vanilla and `DataDog` [statsd](https://github.com/etsy/statsd),
but focused on `DataDog`.


## Usage

 1. Configure a metrics client:

        # either use vanilla statsd
        graph.use("statsd")

        # or use the datadog implementation
        graph.use("datadog_statsd")

 2. In either case, use the resulting `graph.metrics` client:

        metrics.increment("foo")

 3. Better still, use the decorators:

        @graph.metrics_timing
        def my_func():
            pass


## DataDog Testing

First, run the `DataDog Agent` (requires an `API_KEY`). For example, using Docker:

    docker run -d --name datadog-agent -p 8125:8125/udp -e API_KEY=${API_KEY} datadog/docker-dd-agent:latest

Then, use the included CLI to validate connectivity:

    publish-metric --host $(docker-machine ip development)

The resulting metric should appear in `DataDog` "Metric Summary" right away.
