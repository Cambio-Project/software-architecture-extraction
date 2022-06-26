from extractor.r_d_e.librede_host import LibredeHost
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


class LibredeOutputParser:
    def __init__(self, services: list[LibredeServiceOperation], path_to_output_files: str):
        self.services = services
        self.path_to_output_files = path_to_output_files

    def get_results_of_librede(self) -> dict[LibredeServiceOperation, float]:
        resource_demands = dict[LibredeServiceOperation, float]()
        approach_results = self.get_approach_results()  # mapping between approach and result
        # TODO transform results (result for every (host, service)-tuple) into a demand for every single host. (Sum of demands or average?)
        return resource_demands

    def get_approach_results(self) -> dict[str, list[float]]:
        approaches = ["ResponseTimeApproximationApproach", "ServiceDemandLawApproach", "WangKalmanFilterApproach", "ZhangKalmanFilterApproach"]
        approach_results = dict[str, list[float]]()  # mapping between approach to its results
        for approach in approaches:
            output_file_handler = open(self.path_to_output_files + "estimates_" + approach + "_fold_0.csv")
            output_file_content = output_file_handler.read()
            estimations_as_str = output_file_content.split(",")
            estimations = list[float]()
            for i in range(1, len(estimations_as_str)):
                estimations.append(float(estimations_as_str[i]))
            approach_results[approach] = estimations
        return approach_results
