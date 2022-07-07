import os

from extractor.arch_models.model import IModel
from extractor.r_d_e.librede_configuration_creator import LibredeConfigurationCreator
from extractor.r_d_e.librede_host import LibredeHost, get_hosts
from extractor.r_d_e.default_cpu_utilization import get_default_cpu_utilization
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation, get_operations


class LibredeInputCreator:
    """
    Creates all necessary .csv-Files and the LibReDE-Configuration-file at instantiation.
    """

    # Creates the output paths, the .csv-Files and the LibReDE_Configuration-File.
    def __init__(self, model: IModel, path_for_librede_files: str):
        self.hosts: list[LibredeHost] = get_hosts(model)
        self.operations_on_host: list[LibredeServiceOperation] = get_operations(model, self.hosts)
        add_default_cpu_utilization(self.hosts)
        for librede_service_operation in self.operations_on_host:
            librede_service_operation.clean_response_times()

        self.absolute_path_to_input: str = path_for_librede_files + "input\\"
        self.absolute_path_to_output: str = path_for_librede_files + "output\\"
        self.set_indices_to_hosts_and_services()
        self.configuration = LibredeConfigurationCreator(self.hosts, self.operations_on_host,
                                                         self.absolute_path_to_input, self.absolute_path_to_output,
                                                         self.get_start_timestamp(), self.get_end_timestamp())
        # Create necessary directories, in case they don't exist.
        if not os.path.exists(path_for_librede_files):
            os.mkdir(path_for_librede_files)
        if not os.path.exists(self.absolute_path_to_input):
            os.mkdir(self.absolute_path_to_input)
        if not os.path.exists(self.absolute_path_to_output):
            os.mkdir(self.absolute_path_to_output)
        self.create_csv_files()

    # Creates all .csv-Files necessary for LibReDE.
    def create_csv_files(self):
        # Create cpu_utilization-files for all hosts
        for host in self.hosts:
            new_csv_file_handler = open(self.absolute_path_to_input + host.get_csv_file_name(), "w")
            new_csv_file_handler.write(host.get_csv_file_content())

        # Create response_times-files for all distinct operation, host pairs
        i = 0
        for operation in self.operations_on_host:
            new_csv_file_handler = open(self.absolute_path_to_input + operation.get_csv_file_name(), "w")
            new_csv_file_handler.write(operation.get_csv_file_content())
            i += 1

        # Creates LibReDE_Configuration-Files
        new_csv_file_handler = open(self.absolute_path_to_input + self.configuration.get_file_name(), "w")
        new_csv_file_handler.write(self.configuration.get_xml_content())

    # Gives each service and host and index (not unique between hosts and services).
    # LibReDE needs them for unambiguous identification.
    def set_indices_to_hosts_and_services(self):
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

    def get_path_to_configuration_file(self):
        return self.configuration.get_path_to_configuration_file()

    def __str__(self) -> str:
        string_representation = ""
        for host in self.hosts:
            string_representation += "host: " + str(host) + "\n"
        for operation in self.operations_on_host:
            string_representation += str(operation) + "\n"
        return string_representation


# adds a default cpu utilization to all hosts
def add_default_cpu_utilization(all_hosts: list[LibredeHost]):
    for host in all_hosts:
        host.cpu_utilization = get_default_cpu_utilization(host.start_time, host.end_time)
