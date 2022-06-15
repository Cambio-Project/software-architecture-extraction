from extractor.arch_models.model import IModel


# Representation of an operation of a service for LibReDE.
#
# A service in LibReDE is an operation of a service in the generic model.
# A service can have multiple instances, so an operation of a service can be processed on different hosts.
# For each distinct operation, host pair a new instance of a LibredeServiceOperation is created.
class LibredeServiceOperation:

    def __init__(self, operation_name: str, host):
        self.operation_name = operation_name
        self.id = -1
        self.host = host
        self.response_times = []

    # Adds a new response time to this service.
    def add_response_time(self, response_time: tuple[int, int]):
        self.response_times.append(response_time)

    def get_csv_file_name(self) -> str:
        return "operation" + str(self.id) + "_response_times.csv"

    # Transforms the response-times in a .csv-format for LibReDE looking like:
    # <time0>,<response-time0>\n<time1>,<response-time1> etc.
    def get_csv_file_content(self) -> str:
        csv_file_content = ""
        for response_time_entry in self.response_times:
            csv_file_content += str(response_time_entry[0]) + "," + str(response_time_entry[1]) + "\n"
        return csv_file_content

    def __str__(self):
        string_representation = "<" + self.operation_name + ">-operation at host: <" + self.host.name + "> with "
        string_representation += str(len(self.response_times)) + " " + (
            "calls" if len(self.response_times) > 1 or len(self.response_times) == 0 else "call")
        return string_representation


# Iterates over all operations of the model creates a LibredeServiceOperation object for each distinct
# operation, host pair
def get_operations(model: IModel, hosts):
    all_operations_on_hosts = []
    for service in model.services.values():
        for operation in service.operations.values():
            hosts_of_operation = operation.response_times.keys()
            for host in hosts_of_operation:
                # get the Librede host object of the host of this operation
                librede_host = get_host(host, hosts)

                if librede_host is None:
                    print("Host not found")
                    continue

                operation_for_librede = LibredeServiceOperation(operation.name, librede_host)

                # get the response times from the model
                response_times = operation.response_times[host]

                # calculate the minimum and the maximum timestamps of the response time entries
                # if they exceed the current boundaries of the corresponding host the boundaries are updated
                minimum_timestamp = get_minimum_timestamp(response_times)
                maximum_timestamp = get_maximum_timestamp(response_times)

                if minimum_timestamp < librede_host.start_time:
                    librede_host.start_time = minimum_timestamp
                if maximum_timestamp > librede_host.end_time:
                    librede_host.end_time = maximum_timestamp

                operation_for_librede.response_times.extend(response_times)
                all_operations_on_hosts.append(operation_for_librede)

    return all_operations_on_hosts


# Searches a Librede host by its name and returns it
def get_host(hostname, hosts):
    for host in hosts:
        if host.name == hostname:
            return host


# returns the minimum timestamp of a list of (timestamp, response time) pairs
def get_minimum_timestamp(times):
    minimum = times[0][0]
    for time_pair in times:
        if time_pair[0] < minimum:
            minimum = time_pair[0]
    return minimum


# returns the maximum timestamp of a list of (timestamp, response time) pairs
def get_maximum_timestamp(times):
    maximum = times[0][0]
    for time_pair in times:
        if time_pair[0] > maximum:
            maximum = time_pair[0]
    return maximum


