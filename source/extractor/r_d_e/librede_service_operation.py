from extractor.arch_models.model import IModel
from extractor.arch_models.service import Service


class LibredeServiceOperation:
    """
    Representation of an operation of a service for LibReDE.
    A service in LibReDE is an operation of a service in the generic model.
    A service can have multiple instances, so an operation of a service can be processed on different hosts.
    For each distinct operation, host pair a new instance of a LibredeServiceOperation is created.
    """

    def __init__(self, operation_name: str, host, service: Service):
        self.operation_name = operation_name  # name of the operation this represents.
        self.id = -1  # id for unambiguous identification for LibReDE, will be set later.
        self.host = host  # LibReDEHost which ran this operation.
        self.service = service  # The Service-Object which contains this operation.
        self.response_times = list[tuple[float, float]]()  # list of <time, response-time of query>

    def get_csv_file_name(self) -> str:
        return "operation_id" + str(self.id) + "_response_times.csv"

    def get_csv_file_content(self) -> str:
        """
        Transforms the response-times in a .csv-format for LibReDE looking like:
        <time0>,<response-time0>\n<time1>,<response-time1> etc.
        Needs to be done with a list, because concatenation of many, long strings reduces the performance.
        """
        csv_file_content_elements = list[str]()
        for response_time_entry in self.response_times:
            csv_file_content_elements.append(str(response_time_entry[0]) + "," + str(response_time_entry[1]) + "\n")
        return "".join(csv_file_content_elements)

    def __str__(self):
        string_representation = "operation: <" + self.operation_name + "> (id " + str(self.id) + ") at host: <" + self.host.name + "> with "
        string_representation += str(len(self.response_times)) + " " + ("response-time-entries" if len(self.response_times) > 1 or len(self.response_times) == 0 else "response-time-entry")
        return string_representation

    def __hash__(self):
        return hash((self.operation_name, self.service.name))

    def __eq__(self, other):
        return (self.operation_name, self.service.name) == (other.operation_name, other.service.name)

    def clean_response_times(self):
        """
        Sorts the response times and converts the time stamps and response times to seconds (while remaining the milliseconds).
        """
        self.response_times = sorted(self.response_times, key=lambda response_time_entry: response_time_entry[0])
        for i in range(len(self.response_times)):
            current_response_time_entry = self.response_times[i]
            new_time = int(current_response_time_entry[0] / 10 ** 3) / 10 ** 3
            new_response_time = current_response_time_entry[1] / 10 ** 6
            self.response_times[i] = (new_time, new_response_time)


def get_operations(model: IModel, hosts):
    """
    Iterates over all operations of the model creates a LibredeServiceOperation object for each distinct
    operation, host pair
    """
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

                operation_for_librede = LibredeServiceOperation(operation.name, librede_host, service)
                librede_host.add_service(operation_for_librede)

                # get the response times from the model
                response_times = operation.response_times[host]

                # calculate the minimum and the maximum timestamps of the response time entries
                # if they exceed the current boundaries of the corresponding host, the boundaries are updated
                minimum_timestamp = get_minimum_timestamp(response_times)
                maximum_timestamp = get_maximum_timestamp(response_times)

                if minimum_timestamp < librede_host.start_time:
                    librede_host.start_time = minimum_timestamp
                if maximum_timestamp > librede_host.end_time:
                    librede_host.end_time = maximum_timestamp

                operation_for_librede.response_times.extend(response_times)
                all_operations_on_hosts.append(operation_for_librede)

    return all_operations_on_hosts


def get_host(hostname, hosts):
    """
    Searches a LibReDEHost by its name and returns it.
    Returns None if there is no host with the given name.
    """
    for host in hosts:
        if host.name == hostname:
            return host
    return None


def get_minimum_timestamp(times):
    """
    Returns the minimum timestamp of a list of (timestamp, response time) pairs
    """
    minimum = times[0][0]
    for time_pair in times:
        if time_pair[0] < minimum:
            minimum = time_pair[0]
    return minimum


def get_maximum_timestamp(times):
    """
    Returns the maximum timestamp of a list of (timestamp, response time) pairs
    """
    maximum = times[0][0]
    for time_pair in times:
        if time_pair[0] > maximum:
            maximum = time_pair[0]
    return maximum
