import sys

from extractor.arch_models.model import IModel
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


class LibredeHost:
    """
    Representation of a Host for LibReDE (e.g. a container running an instance of a service).
    It's characterized by its cpu_utilization between start_time and end_time.
    The cpu_utilization and start_-/end_time has to be set manually.
    """

    def __init__(self, name: str):
        self.name: str = name  # name of the process in the trace.
        self.id = -1  # id for unambiguous identification for LibReDE, will be set later.
        self.services = list[LibredeServiceOperation]()  # Operations which runs on this host, will be updated later.
        self.start_time = sys.maxsize  # represents the lower bound of the activeness of this host, will be updated later.
        self.end_time = -1  # represents the upper bound of activeness of this host, will be updated later.
        self.cpu_utilization = list[tuple[int, float]]()  # list of <time, utilization>-entries.

    def add_service(self, operation: LibredeServiceOperation):
        """
        Adds an operation to this, that means the given operation ran on this at least once.
        """
        self.services.append(operation)

    def get_csv_file_name(self) -> str:
        return "host_" + str(self.id) + "_cpu_utilization.csv"

    def get_csv_file_content(self) -> str:
        """
        Parses the cpu-utilization in a .csv-format for LibReDE looking like:
        <time0>,<cpu_utilization0>\n<time1>,<cpu_utilization1> etc.
        Needs to be done with a list, because concatenation of many, long strings reduces the performance.
        """
        csv_file_content = list[str]()
        for cpu_utilization_entry in self.cpu_utilization:
            csv_file_content.append(str(cpu_utilization_entry[0]) + "," + str(cpu_utilization_entry[1]) + "\n")
        return "".join(csv_file_content)

    def __str__(self) -> str:
        return "<" + self.name + "> (id " + str(self.id) + ") with " + str(len(self.cpu_utilization)) + " cpu-utilization-entries."


def get_hosts(model: IModel) -> list[LibredeHost]:
    """
    Gets all hosts of the generic model and creates a LibReDE host for each one.
    """
    all_hosts = []
    for service in model.services.values():
        for host in service.hosts:
            if not all_hosts.__contains__(host):
                all_hosts.append(host)
    hosts_for_librede = []
    for host in all_hosts:
        hosts_for_librede.append(LibredeHost(host))
    return hosts_for_librede
