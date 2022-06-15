import sys

from extractor.arch_models.model import IModel
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


# Representation of a Host for LibReDE (e.g. a container running an instance of a service).
class LibredeHost:

    def __init__(self, name: str):
        self.name: str = name  # name of the process in the trace
        self.id = -1  # id for unambiguous identification for LibReDE, will be set later
        self.services = []
        self.start_time = sys.maxsize
        self.end_time = -1
        self.cpu_utilization = []

    # Adds the service to the services of this host.
    # This means that a span was found in which an operation (service) ran on this.
    def add_service(self, operation: LibredeServiceOperation):
        self.services.append(operation)

    def get_csv_file_name(self) -> str:
        return "host" + str(self.id) + "_cpu_utilization.csv"

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


# Gets all hosts of the generic model and creates a Librede host for each one
def get_hosts(model: IModel) -> list[LibredeHost]:
    all_hosts = []
    for service in model.services.values():
        for host in service.hosts:
            if not all_hosts.__contains__(host):
                all_hosts.append(host)

    hosts_for_librede = []
    for host in all_hosts:
        hosts_for_librede.append(LibredeHost(host))

    return hosts_for_librede