from extractor.r_d_e.default_cpu_utilization import get_default_cpu_utilization


# Representation of a Host for LibReDE (basically equivalent to a process in a trace)
#
# Initialized with default cpu-utilization.
class LibReDE_Host:

    def __init__(self, name: str, start_time: int, end_time: int):
        self.name: str = name
        self.cpu_utilization = get_default_cpu_utilization(start_time, end_time)

    def __str__(self):
        return self.name + " with " + str(len(self.cpu_utilization)) + " cpu-utilization-entries."


def get_hosts_with_default_cpu_utilization(trace) -> list[LibReDE_Host]:
    hosts = list[LibReDE_Host]()
    processes = trace["data"][0]["processes"]
    start_time_of_trace = trace["data"][0]["spans"][0]["startTime"]
    last_span = trace["data"][0]["spans"][len(trace["data"][0]["spans"]) - 1]
    end_time_of_trace = last_span["startTime"] + last_span["duration"]
    for process_id, process in processes.items():
        hosts.append(LibReDE_Host(process_id, start_time_of_trace, end_time_of_trace))
    return hosts
