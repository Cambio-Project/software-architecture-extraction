import os

from extractor.r_d_e.librede_configuration_creator import LibReDE_ConfigurationCreator
from extractor.r_d_e.librede_host import LibReDE_Host, get_hosts_with_default_cpu_utilization
from extractor.r_d_e.librede_service import LibReDE_Service, get_services


# Creates all necessary .csv-Files at instantiation.
class LibReDE_Input_Creator:

    def __init__(self, trace):
        self.trace = trace
        self.hosts: list[LibReDE_Host] = get_hosts_with_default_cpu_utilization(trace)
        self.services: list[LibReDE_Service] = extract_list_of_services(get_services(trace, self.hosts))
        fill_indices(self.hosts, self.services)
        self.configuration = LibReDE_ConfigurationCreator(self.hosts, self.services)
        if not os.path.exists("C:\\Users\\Gabriel\\Desktop\\r-d-e_input\\"):
            os.mkdir("C:\\Users\\Gabriel\\Desktop\\r-d-e_input\\")
        create_csv_files_at("C:\\Users\\Gabriel\\Desktop\\r-d-e_input\\", self.hosts, self.services, self.configuration)

    def __str__(self) -> str:
        string_representation = ""
        for host in self.hosts:
            string_representation += "host: " + str(host) + "\n"
        string_representation += "----------------------\n"
        for service in self.services:
            string_representation += str(service) + "\n"
        return string_representation


# Creates all .csv-Files out of the given hosts and services.
def create_csv_files_at(location: str, hosts: list[LibReDE_Host], services: list[LibReDE_Service], configuration: LibReDE_ConfigurationCreator):
    for host in hosts:
        new_csv_file = open(location + host.get_csv_file_name(), "w")
        new_csv_file.write(host.get_csv_file_content())
    for service in services:
        new_csv_file = open(location + service.get_csv_file_name(), "w")
        new_csv_file.write(service.get_csv_file_content())
    new_csv_file = open(location + configuration.get_csv_name(), "w")
    new_csv_file.write(configuration.content)


def extract_list_of_services(services: dict[str, list[LibReDE_Service]]) -> list[LibReDE_Service]:
    services_list = list[LibReDE_Service]()
    for key in services.keys():
        for single_service in services[key]:
            services_list.append(single_service)
    return services_list


def fill_indices(hosts: list[LibReDE_Host], services: list[LibReDE_Service]):
    i = 0
    for host in hosts:
        host.index = i
        i += 1
    i = 0
    for service in services:
        service.index = i
        i += 1
