# Calculates the start and endtime of a trace by looking at the first and the last span.
def get_start_and_end_time(trace) -> tuple[int, int]:
    spans = trace["data"][0]["spans"]
    start_time_of_trace = spans[0]["startTime"]
    last_span = spans[len(spans) - 1]
    end_time_of_trace = last_span["startTime"] + last_span["duration"]
    return start_time_of_trace, end_time_of_trace
