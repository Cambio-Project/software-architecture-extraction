from extractor.arch_models.jaeger_trace import JaegerTrace
from extractor.arch_models.zipkin_trace import ZipkinTrace
from extractor.r_d_e.librede_caller import call_librede
from input.InteractiveTraceInput import InteractiveTraceInput

# Manual test with jaeger given jaeger trace
trace_input = InteractiveTraceInput()
generic_model = None
if trace_input.traces_are_jaeger:
    generic_model = JaegerTrace(trace_input.traces, trace_input.contains_multiple_traces, None)
elif trace_input.traces_are_zipkin:
    generic_model = ZipkinTrace(trace_input.traces, trace_input.contains_multiple_traces, None)
call_librede(generic_model)
