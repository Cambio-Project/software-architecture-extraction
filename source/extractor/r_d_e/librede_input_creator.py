import os

from extractor.arch_models.model import IModel
from extractor.r_d_e.librede_configuration_creator import LibredeConfigurationCreator, create_configurations
from extractor.r_d_e.librede_host import LibredeHost, get_hosts
from extractor.r_d_e.default_cpu_utilization import get_default_cpu_utilization
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation, get_operations
from input.input_utils import get_valid_string_input_with_predicates, str_is_float, get_valid_float_input, get_valid_file_path_input, read_csv


class LibredeInputCreator:
    """
    Creates all necessary .csv-Files and configurations at instantiation.
    """

    def __init__(self, model: IModel, path_to_librede_files: str, approaches: list[str]):
        self.model = model
        self.approaches = approaches
        self.hosts: list[LibredeHost] = get_hosts(model)
        self.operations_on_host: list[LibredeServiceOperation] = get_operations(model, self.hosts)
        add_cpu_utilization(self.hosts)
        for librede_service_operation in self.operations_on_host:
            librede_service_operation.clean_response_times()
        self.absolute_path_to_input: str = path_to_librede_files + "input" + os.path.sep
        self.absolute_path_to_output: str = path_to_librede_files + "output" + os.path.sep
        self.set_indices_to_hosts_and_services()
        self.configurations: list[LibredeConfigurationCreator] = create_configurations(self.operations_on_host, approaches,
                                                                                       self.absolute_path_to_input, self.absolute_path_to_output)
        # Create necessary directories, in case they don't exist.
        if not os.path.exists(path_to_librede_files):
            os.mkdir(path_to_librede_files)
        if not os.path.exists(self.absolute_path_to_input):
            os.mkdir(self.absolute_path_to_input)
        if not os.path.exists(self.absolute_path_to_output):
            os.mkdir(self.absolute_path_to_output)
        self.create_csv_files()

    def create_csv_files(self):
        # Create cpu_utilization-csv-files for all hosts
        for host in self.hosts:
            new_csv_file_handler = open(self.absolute_path_to_input + host.get_csv_file_name(), "w")
            new_csv_file_handler.write(host.get_csv_file_content())
            new_csv_file_handler.close()
        # Create response_times-csv-files for all distinct operation, host pairs
        for operation in self.operations_on_host:
            new_csv_file_handler = open(self.absolute_path_to_input + operation.get_csv_file_name(), "w")
            new_csv_file_handler.write(operation.get_csv_file_content())
            new_csv_file_handler.close()
        # Creates LibReDE_Configuration-Files
        for configuration in self.configurations:
            new_csv_file_handler = open(self.absolute_path_to_input + configuration.get_file_name(), "w")
            new_csv_file_handler.write(configuration.get_xml_content())
            new_csv_file_handler.close()

    def set_indices_to_hosts_and_services(self):
        """
        Gives each service and host and index (not unique between hosts and services).
        LibReDE needs them for unambiguous identification.
        """
        i = 0
        for host in self.hosts:
            host.id = i
            i += 1
        i = 0
        for operation in self.operations_on_host:
            operation.id = i
            i += 1

    def get_start_timestamp(self) -> int:
        minimum = self.hosts[0].start_time
        for host in self.hosts:
            if host.start_time < minimum:
                minimum = host.start_time
        return minimum

    def get_end_timestamp(self) -> int:
        maximum = self.hosts[0].end_time
        for host in self.hosts:
            if host.end_time > maximum:
                maximum = host.end_time
        return maximum

    def print_summary_of_input(self):
        for host in self.hosts:
            print("host: " + str(host))
        for operation in self.operations_on_host:
            print(str(operation))


def add_cpu_utilization(all_hosts: list[LibredeHost]):
    answer = get_valid_string_input_with_predicates("Set cpu-utilization for LibReDE.",
                                                    ["number in [0, 1] (will be default for all hosts)",
                                                     "\"manual\" (set fix utilization for each host manually)",
                                                     "\"csv\" (set csv with utilizations for each host)"],
                                                    [lambda a: str_is_float(a),
                                                     lambda a: a == "manual",
                                                     lambda a: a == "csv"])
    option_the_user_decided_for = answer[0]
    user_input = answer[1]
    if option_the_user_decided_for == 0:
        for host in all_hosts:
            host.cpu_utilization = get_default_cpu_utilization(host.start_time, host.end_time, float(user_input))
    elif option_the_user_decided_for == 1:
        for host in all_hosts:
            host.cpu_utilization = get_default_cpu_utilization(host.start_time, host.end_time, get_valid_float_input("Set cpu utilization for host <" + host.name + ">."))
    else:
        for host in all_hosts:
            csv_file_path = get_valid_file_path_input("Path to cpu utiliztation csv-file for host <" + host.name + ">")
            cpu_progress = read_csv(csv_file_path)
            for row in cpu_progress:
                timestamp = int(float(row[0]))
                utilization = float(row[1])
                host.cpu_utilization.append((timestamp, utilization))
