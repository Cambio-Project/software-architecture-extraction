from extractor.r_d_e.default_cpu_utilization import get_default_cpu_utilization


# Representation of a Host for LibReDE (basically equivalent to a process in a trace).
# Contains the name of the process this represents and the cpu-utilization as a list of tuples (time,cpu-utilization).
class LibReDE_Host:

    def __init__(self, name: str, cpu_utilization: list[tuple[int, float]]):
        self.name: str = name  # name of the process in the trace
        self.index = -1  # index for unambiguous identification for LibReDE, will be set later
        self.services = list()
        self.cpu_utilization = cpu_utilization

    # Adds the service to the services of this host.
    # This means that a span was found in which an operation (service) ran on this.
    def add_service(self, service):
        self.services.append(service)

    def get_csv_file_name(self) -> str:
        return self.name + "_cpu_utilization.csv"

    # Parses the cpu-utilization in a .csv-format for LibReDE looking like:
    # <time0>,<cpu_utilization0>\n<time1>,<cpu_utilization1> etc.
    def get_csv_file_content(self) -> str:
        csv_file_content = ""
        for cpu_utilization_entry in self.cpu_utilization:
            time = cpu_utilization_entry[0]
            current_cpu_utilization = cpu_utilization_entry[1]
            csv_file_content += str(time) + "," + str(current_cpu_utilization) + "\n"
        return csv_file_content

    def __str__(self) -> str:
        return self.name + " with " + str(len(self.cpu_utilization)) + " cpu-utilization-entries."


def get_hosts_with_default_cpu_utilization(trace) -> list[LibReDE_Host]:
    hosts = list[LibReDE_Host]()
    processes = trace["data"][0]["processes"]
    start_time_of_trace = trace["data"][0]["spans"][0]["startTime"]
    last_span = trace["data"][0]["spans"][len(trace["data"][0]["spans"]) - 1]
    end_time_of_trace = last_span["startTime"] + last_span["duration"]
    default_cpu_utilization = get_default_cpu_utilization(start_time_of_trace, end_time_of_trace)
    for process_id, process in processes.items():
        hosts.append(LibReDE_Host(process_id, default_cpu_utilization))
    return hosts
