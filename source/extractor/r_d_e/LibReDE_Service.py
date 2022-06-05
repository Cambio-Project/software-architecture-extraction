from extractor.r_d_e.LibReDE_Host import LibReDE_Host


# Representation of a service for LibReDE.
#
# A service is basically an operation of a trace. However, a service in LibReDE is only allowed to be processed by a single host.
# Therefore, if an operation is processed by several hosts (two spans with the same <operationName>, but different <processID>), more LibReDE_Service instances
# for an operation are needed.
class LibReDE_Service:

    def __init__(self, operation_name: str, host: LibReDE_Host):
        self.operation_name = operation_name
        self.host = host
        self.response_times = list[tuple[int, int]]()

    def add_response_time(self, response_time: tuple[int, int]):
        self.response_times.append(response_time)

    def get_csv_file_name(self) -> str:
        return self.operation_name + "_" + self.host.name + "_response_times.csv"

    def get_csv_file_content(self) -> str:
        csv_file_content = ""
        for response_time_entry in self.response_times:
            csv_file_content += str(response_time_entry[0]) + "," + str(response_time_entry[1]) + "\n"
        return csv_file_content

    def __str__(self):
        string_representation = "<" + self.operation_name + ">-operation at host: <" + self.host.name + "> with "
        string_representation += str(len(self.response_times)) + " " + ("calls" if len(self.response_times) > 1 or len(self.response_times) == 0 else "call")
        return string_representation


# Iterates over all spans and adds a tuple (time, response_time) in each iteration to the respective service.
def get_services(trace, hosts: list[LibReDE_Host]) -> dict[str, list[LibReDE_Service]]:
    spans = trace["data"][0]["spans"]
    # Mapping between the operation_name and all its services.
    found_services = dict[str, list[LibReDE_Service]]()
    for span in spans:
        service_to_update = get_single_service_to_update(span, hosts, found_services)
        new_response_time = (span["startTime"], span["duration"])
        service_to_update.add_response_time(new_response_time)
    return found_services


# Retrieves the service to which the new (time, response-time)-entry needs to be added to.
def get_single_service_to_update(span, hosts, all_found_services) -> LibReDE_Service:
    operation_name: str = span["operationName"]
    process_id: str = span["processID"]
    host: LibReDE_Host = get_host_with_name(process_id, hosts)
    # Registers the operation in the dict, if it hasn't been registered, yet.
    if not all_found_services.keys().__contains__(operation_name):
        all_found_services[operation_name] = list[LibReDE_Service]()
    existing_services_of_operation = all_found_services[operation_name]
    # Returns the respective service if the operation has already been called on the given host.
    if has_service_with_host(process_id, existing_services_of_operation):
        return get_service_with_host(process_id, existing_services_of_operation)
    # Creates a new service of the existing operation but with the new host.
    else:
        new_service = LibReDE_Service(operation_name, host)
        existing_services_of_operation.append(new_service)
        return new_service


# Returns the LibReDE_Host with the given name out of the given list.
def get_host_with_name(host_name: str, hosts: list[LibReDE_Host]) -> LibReDE_Host:
    for host in hosts:
        if host.name == host_name:
            return host
    raise Exception("No host named: " + host_name + " in " + str([host.name for host in hosts]))


# Returns True if the given list of LibReDE_Service contains a LibReDE_Service with the given LibReDE_Host-name, else False.
def has_service_with_host(host_name: str, services: list[LibReDE_Service]) -> bool:
    for service in services:
        if service.host.name == host_name:
            return True
    return False


# Returns the LibReDE_Service with the given LibReDE_Host-name out of the given list.
def get_service_with_host(host_name: str, services: list[LibReDE_Service]) -> LibReDE_Service:
    for service in services:
        if service.host.name == host_name:
            return service
    raise Exception("No service with host: " + host_name + " in " + str([str(service) for service in services]))
