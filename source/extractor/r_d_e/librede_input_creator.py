import os

from extractor.r_d_e.librede_configuration_creator import LibReDE_ConfigurationCreator
from extractor.r_d_e.librede_host import LibReDE_Host, get_hosts_with_default_cpu_utilization
from extractor.r_d_e.librede_service import LibReDE_Service, get_services

# Extracts all services out of the given dictionary.
from extractor.r_d_e.util import get_start_and_end_time


def extract_list_of_services(services: dict[str, list[LibReDE_Service]]):
    services_list = list[LibReDE_Service]()
    for key in services.keys():
        for single_service in services[key]:
            services_list.append(single_service)
    return services_list


# Creates all necessary .csv-Files and the LibReDE-Configuration at instantiation.
class LibReDE_InputCreator:

    # Creates the output paths, the .csv-Files and the LibReDE_Configuration-File.
    def __init__(self, trace, path_for_librede_files: str):
        self.trace = trace
        self.hosts: list[LibReDE_Host] = get_hosts_with_default_cpu_utilization(trace)
        self.services: list[LibReDE_Service] = extract_list_of_services(get_services(trace, self.hosts))
        self.absolute_path_to_input: str = path_for_librede_files + "input\\"
        self.absolute_path_to_output: str = path_for_librede_files + "output\\"
        self.set_indices_to_hosts_and_services()
        start_and_end_time = get_start_and_end_time(trace)
        self.configuration = LibReDE_ConfigurationCreator(self.hosts, self.services, start_and_end_time[0], start_and_end_time[1], self.absolute_path_to_input, self.absolute_path_to_output)
        # Create necessary directories, in case they don't exist, yet.
        if not os.path.exists(path_for_librede_files):
            os.mkdir(path_for_librede_files)
        if not os.path.exists(self.absolute_path_to_input):
            os.mkdir(self.absolute_path_to_input)
        if not os.path.exists(self.absolute_path_to_output):
            os.mkdir(self.absolute_path_to_output)
        self.create_csv_files()

    # Creates all .csv-Files necessary for LibReDE.
    def create_csv_files(self):
        # Create cpu_utilization-files for all processes
        for host in self.hosts:
            new_csv_file = open(self.absolute_path_to_input + host.get_csv_file_name(), "w")
            new_csv_file.write(host.get_csv_file_content())
        # Create response_times-files for all services.
        for service in self.services:
            new_csv_file = open(self.absolute_path_to_input + service.get_csv_file_name(), "w")
            new_csv_file.write(service.get_csv_file_content())
        # Creates LibReDE_Configuration-Files
        new_csv_file = open(self.absolute_path_to_input + self.configuration.get_file_name(), "w")
        new_csv_file.write(self.configuration.content)

    # Gives each service and host and index (not unique between hosts and services).
    # LibReDE needs them for unambiguous identification.
    def set_indices_to_hosts_and_services(self):
        i = 0
        for host in self.hosts:
            host.index = i
            i += 1
        i = 0
        for service in self.services:
            service.index = i
            i += 1

    def get_path_to_configuration_file(self):
        return self.configuration.get_path_to_configuration_file()

    def __str__(self) -> str:
        string_representation = ""
        for host in self.hosts:
            string_representation += "host: " + str(host) + "\n"
        string_representation += "----------------------\n"
        for service in self.services:
            string_representation += str(service) + "\n"
        return string_representation
