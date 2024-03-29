import math

import numpy as np

from extractor.arch_models.model import IModel
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation
from input.input_utils import get_valid_yes_no_input


class LibredeOutputParser:
    """
    Class which parses the output of LibReDE.
    Will calculate the final estimated utilization_demand as the average of all approaches the user wants to use.
    """

    def __init__(self, service_operations: list[LibredeServiceOperation], path_to_output_files: str, approaches: list[str], model: IModel):
        self.model = model
        self.service_operations = service_operations
        self.possible_approaches = approaches
        self.path_to_output_files = path_to_output_files
        self.final_results = self.calcualate_results_of_librede()

    def get_results_of_librede(self) -> dict[tuple[str, str], float]:
        return self.final_results

    def calcualate_results_of_librede(self) -> dict[tuple[str, str], float]:
        """
        Calculates a mapping between [service_name, operation_name] to its estimated utilization by the approaches
        the user wanted to use. (The final result is the average of the estimations by the desired approaches)
        """
        original_output: dict[LibredeServiceOperation, dict[str, float]] = self.parse_output_of_librede()
        mapped_output: dict[tuple[str, str], dict[str, float]] = self.map_output(original_output)
        self.print_results_of_librede(mapped_output)
        print("-------------------------------------------------")
        approaches_to_use = self.get_approaches_to_use()
        final_results = dict[tuple[str, str], float]()
        for unique_operation in mapped_output:
            sum = 0
            number_of_valid_results = len(approaches_to_use)
            for approach in approaches_to_use:
                if np.isnan(mapped_output[unique_operation][approach]) or mapped_output[unique_operation][approach] < 0:
                    number_of_valid_results -= 1
                else:
                    sum += mapped_output[unique_operation][approach]
            final_results[unique_operation] = sum / number_of_valid_results if number_of_valid_results > 0 else math.nan
        print("------------------------------------------------- Finished calculating the resource demands")
        return final_results

    def map_output(self, original_output: dict[LibredeServiceOperation, dict[str, float]]) -> dict[tuple[str, str], dict[str, float]]:
        """
        Maps the original output to a mapping between [service_name, operation_name] to [a mapping between approach to its estimation].
        Will be calculated by taking the average of the estimations of a single operation on several hosts.
        """
        structured_original_output = dict[tuple[str, str], list[dict[str, float]]]()
        for service_operation in original_output.keys():
            unique_name = (service_operation.service.name, service_operation.operation_name)
            if not structured_original_output.keys().__contains__(unique_name):
                structured_original_output[unique_name] = list[dict[str, float]]()
            structured_original_output[unique_name].append(original_output[service_operation])
        results = dict[tuple[str, str], dict[str, float]]()
        for unique_operation in structured_original_output.keys():
            estimations_on_all_hosts: list[dict[str, float]] = structured_original_output[unique_operation]
            average_estimations = dict[str, float]()
            for approach in self.possible_approaches:
                sum = 0
                service = unique_operation[0]
                number_of_valid_results = len(self.model.services[service].hosts)
                for estimation_results_on_single_host in estimations_on_all_hosts:
                    if np.isnan(estimation_results_on_single_host[approach]) or estimation_results_on_single_host[approach] < 0:
                        number_of_valid_results -= 1
                    else:
                        sum += estimation_results_on_single_host[approach]
                average_estimations[approach] = sum / number_of_valid_results if number_of_valid_results > 0 else math.nan
            results[unique_operation] = average_estimations
        return results

    def parse_output_of_librede(self) -> dict[LibredeServiceOperation, dict[str, float]]:
        """
        Retrieves the data from the output-csv-files of LibReDE and stores them in a mapping between LibredeServiceOperation and
        [a mapping between approach and its estimation]. This method simply parses the content of the output .csv-files into
        a format which can be manipulated easier.
        """
        results_of_approaches_per_operation_per_host = dict[LibredeServiceOperation, dict[str, float]]()
        for service_operation in self.service_operations:
            results_of_approaches_per_operation_per_host[service_operation] = dict[str, float]()
            for approach_name in self.possible_approaches:
                output_file_handler = open(self.path_to_output_files + str(service_operation.id) + "_" + approach_name + "_fold_0.csv")
                output_file_content: str = output_file_handler.read()
                estimated_utilization = float(output_file_content.split(",")[1])
                results_of_approaches_per_operation_per_host[service_operation][approach_name] = estimated_utilization
                output_file_handler.close()
        return results_of_approaches_per_operation_per_host

    def get_approaches_to_use(self) -> list[str]:
        """
        Calculates a list of approaches. The user decides via command line input which one of the possible approaches is considered.
        """
        approaches_to_use = list[str]()
        for approach in self.possible_approaches:
            user_approach = get_valid_yes_no_input("Use output of approach \"" + approach + "\"?")
            if user_approach:
                approaches_to_use.append(approach)
        return approaches_to_use

    def print_results_of_librede(self, result_of_approaches_per_operation: dict[tuple[str, str], dict[str, float]]):
        print("Results of LibReDE:")
        for unique_operation in result_of_approaches_per_operation:
            result_per_approach = result_of_approaches_per_operation[unique_operation]
            print("   " + unique_operation[0] + "; " + unique_operation[1])
            for approach in result_per_approach.keys():
                print("      " + approach + ": " + str(result_per_approach[approach]))

    def print_final_results(self):
        for unique_operation in self.final_results:
            print("Estimated final demand of <" + unique_operation[1] + "> of service <" + unique_operation[0] + "> = " + str(self.final_results[unique_operation]))
