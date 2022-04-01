import functools

from hazard_elicitation.settings import TRACING

if TRACING:
    from jaeger_client import Config
    from opentelemetry import trace
    from opentelemetry.ext import jaeger, zipkin
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchExportSpanProcessor


def add_trace(is_parent: bool):
    def wrap(func: callable):
        """
        Decorator to enable tracing of a function
        @param func:    The function that is decorated.
        @return:        Returns the value that func produces.
        """

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if TRACING:
                span = Tracer.span(func.__name__, is_parent)
                response = await func(*args, **kwargs)
                span.finish()
                return response
            else:
                return await func(*args, **kwargs)

        return wrapper

    return wrap


class Tracer:
    TRACER = None
    STACK = []

    # @staticmethod
    # def setup(service_name: str):
    #     """
    #     Tracer with Jaeger standalone SDK.
    #     """
    #     config = Config(
    #         config={
    #             'sampler': {
    #                 'type':  'const',
    #                 'param': 1,
    #             },
    #             'logging': False
    #         },
    #         service_name=service_name)
    #     Tracer.TRACER = config.initialize_tracer()

    @staticmethod
    def setup(service_name: str, use_jaeger: bool = True):
        """
        OpenTelemetry tracer with Jaeger or Zipkin exporter.
        @param service_name:    Name of the service.
        @param use_jaeger:      Use jaeger if True, otherwise Zipkin
        """

        if jaeger:
            exporter = jaeger.JaegerSpanExporter(
                service_name=service_name,
                agent_host_name='localhost',
                agent_port=16686)

        else:
            exporter = zipkin.ZipkinSpanExporter(
                service_name=service_name,
                endpoint='http://localhost:9411/api/v2/spans'
            )

        trace.set_tracer_provider(TracerProvider())
        trace.get_tracer_provider().add_span_processor(BatchExportSpanProcessor(exporter))
        Tracer.TRACER = trace.get_tracer(__name__)

    @staticmethod
    def tracer():
        return Tracer.TRACER

    @staticmethod
    def stop():
        for span in Tracer.STACK:
            span.finish()

    @staticmethod
    def span(name: str, is_parent: bool = False):
        parent = Tracer.get_parent()
        if parent:
            span = Tracer.TRACER.start_span(name, child_of=Tracer.get_parent())
        else:
            span = Tracer.TRACER.start_span(name)
        if is_parent:
            Tracer.set_parent(span)
        return span

    @staticmethod
    def set_parent(span):
        return Tracer.STACK.append(span)

    @staticmethod
    def get_parent():
        if len(Tracer.STACK):
            return Tracer.STACK.pop()
        else:
            return None
