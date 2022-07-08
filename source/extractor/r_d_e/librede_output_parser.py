from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


# Class which parses the output of LibReDE.
# Will calculate the final utilization_demand as the average of all approaches.
class LibredeOutputParser:

    def __init__(self, service_operations: list[LibredeServiceOperation], path_to_output_files: str):
        self.service_operations = service_operations
        self.path_to_output_files = path_to_output_files
        self.names_of_approaches = ["ResponseTimeApproximationApproach", "ServiceDemandLawApproach", "WangKalmanFilterApproach"]

    # Calculates a mapping between (service name, operation name) and its demand_utilization.
    def get_results_of_librede(self) -> dict[tuple[str, str], float]:
        results_per_service_operation = self.get_average_of_results_per_service_operation()
        results_per_operation = dict[tuple[str, str], list[float]]()
        for service_operation in results_per_service_operation.keys():
            demand_utilization = results_per_service_operation[service_operation]
            service_name = service_operation.service.name
            operation_name = service_operation.operation_name
            if not results_per_operation.keys().__contains__((service_name, operation_name)):
                results_per_operation[(service_name, operation_name)] = list[float]()
            results_per_operation[(service_name, operation_name)].append(demand_utilization)
        return self.get_averages(results_per_operation)

    # Calculates the mapping between the LibReDEServiceOperation and its demand_utilization.
    def get_average_of_results_per_service_operation(self) -> dict[LibredeServiceOperation, float]:
        demanded_utilizations = dict[LibredeServiceOperation, float]()
        results_of_approaches = self.parse_output_of_librede()
        # Calculates the average result of all approaches
        for service_operation in self.service_operations:
            sum_of_results = 0
            for approach_name in self.names_of_approaches:
                approach_result = results_of_approaches[approach_name]
                index_in_result = service_operation.host.id * len(self.service_operations) + service_operation.id
                sum_of_results += approach_result[index_in_result]
            demanded_utilizations[service_operation] = sum_of_results / len(self.names_of_approaches)
        return demanded_utilizations

    # Takes the average out of the given dict
    def get_averages(self, results: dict[tuple[str, str], list[float]]) -> dict[tuple[str, str], float]:
        results_with_averages = dict[tuple[str, str], float]()
        for service_and_operation_name in results.keys():
            demanded_utilizations: list[float] = results[service_and_operation_name]
            results_with_averages[service_and_operation_name] = sum(demanded_utilizations) / len(demanded_utilizations)
        return results_with_averages

    # Retrieves the data from the output-csv-files of LibReDE and stores them in a mapping between approach and
    # its estimations for every service-operation for every host.
    def parse_output_of_librede(self) -> dict[str, list[float]]:
        results_of_approaches = dict[str, list[float]]()  # mapping between approach_name and its results.
        for approach_name in self.names_of_approaches:
            output_file_handler = open(self.path_to_output_files + approach_name + "_fold_0.csv")
            output_file_content: str = output_file_handler.read()
            estimations_as_str: list[str] = output_file_content.split(",")
            estimations = list[float]()
            for i in range(1, len(estimations_as_str)):  # Don't start at 0, because 0 is a timestamp.
                estimations.append(float(estimations_as_str[i]))
            results_of_approaches[approach_name] = estimations
        return results_of_approaches
