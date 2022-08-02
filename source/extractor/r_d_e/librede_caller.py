import os
import pathlib
import shutil
import numpy as np
import platform

from extractor.arch_models.model import IModel
from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service
from extractor.r_d_e.librede_input_creator import LibredeInputCreator
from extractor.r_d_e.librede_output_parser import LibredeOutputParser
from input.input_utils import get_valid_string_input_with_predicates, get_valid_dir_path_input, get_valid_yes_no_input


class LibredeCaller:
    """
    Class which contains the functionality to extract the input for LibReDE out of a generic model, call LibReDE,
    parse its output and write the gained information back in the generic model (to the field "demand" of an operation).
    All of this automatically happens at instantiation.
    """

    def __init__(self, model: IModel):
        self.approaches = ["ResponseTimeApproximationApproach", "ServiceDemandLawApproach", "WangKalmanFilterApproach"]
        self.relative_path_to_librede_script_file = os.path.sep + "tools.descartes.librede.releng.standalone" + os.path.sep + "target" \
                                                    + os.path.sep + "standalone" + os.path.sep + "console" + os.path.sep
        self.model: IModel = model
        self.path_to_librede_files = str(pathlib.Path(__file__).parent.resolve()) + os.path.sep + "librede_files" + os.path.sep
        self.librede_input_creator: LibredeInputCreator = LibredeInputCreator(self.model, self.path_to_librede_files, self.approaches)
        self.path_to_librede_bat_file: str = self.ask_for_path_of_librede_installation() + self.relative_path_to_librede_script_file

        self.call_librede()
        self.librede_output_parser = LibredeOutputParser(self.librede_input_creator.operations_on_host, self.path_to_librede_files + "output" + os.path.sep, self.approaches)
        self.parse_output_of_librede()

    def call_librede(self):
        """
        Calls LibReDE for each configuration which was created by the LibredeInputCreator.
        LibReDE needs a workaround: The .bat needs to be called from the path where it is and the configurations must be in the same folder.
        That's why the current working directory is changed, later restored and the configuration file gets copied to the location of the
        .bat and then deleted.
        """
        old_dir = os.getcwd()
        for configuration in self.librede_input_creator.configurations:
            shutil.copy(configuration.get_path_to_configuration_file(), self.path_to_librede_bat_file)
        os.chdir(self.path_to_librede_bat_file)
        for configuration in self.librede_input_creator.configurations:
            name_of_script_file = "librede.bat" if platform.system() == "Windows" else "librede.sh"
            command: str = name_of_script_file + " -c " + configuration.get_file_name() + ""
            print("Running \"" + command + "\" for operation \"" + configuration.service_operation.operation_name + "\" on host \"" + configuration.service_operation.host.name + "\"")
            os.system(command)
            os.remove(self.path_to_librede_bat_file + configuration.get_file_name())
        os.chdir(old_dir)

    def ask_for_path_of_librede_installation(self):
        """
        Asks for a path to the cloned librede repository (must already had been builded).
        By typing "help", a helpful message is printed about how to install LibReDE.
        Asks for a path recursively, till a valid path is put in.
        """
        answer_of_user = get_valid_string_input_with_predicates("Path to your LibReDE-installation.",
                                                                ["Path (e.g. " + os.path.join("C:", "Users", "Max", "Downloads", "librede"),
                                                                 "\"help\" for how to install"],
                                                                [lambda a: os.path.isdir(a + self.relative_path_to_librede_script_file), lambda a: a == "help"])
        option_the_user_decided_for = answer_of_user[0]
        user_input = answer_of_user[1]
        if option_the_user_decided_for == 0:
            return user_input
        else:
            self.print_help_for_installing_librede()
            answer_of_user = get_valid_string_input_with_predicates("Path to your LibReDE-installation.", ["Path"],
                                                                    [lambda a: os.path.isdir(a + self.relative_path_to_librede_script_file)])
            return answer_of_user[1]

    def parse_output_of_librede(self):
        """
        Extracts the necessary information out of the output of LibReDE and adds the demands in the generic model.
        """
        results_of_librede: dict[tuple[str, str], float] = self.librede_output_parser.get_results_of_librede()
        for service_name, operation_name in results_of_librede.keys():
            self.add_demand_to_operation(service_name, operation_name, results_of_librede[(service_name, operation_name)])

    def add_demand_to_operation(self, service_name, operation_name, estimated_demand: float):
        """
        Sets the demand of an operation of a service by multiplying the estimated utilization with the capacity of the service.
        Won't do anything if demanded_utilization is NaN
        """
        if not np.isnan(estimated_demand):
            service: Service = self.get_service(service_name)
            operation: Operation = self.get_operation(operation_name, service)
            demand = int(estimated_demand * service.capacity)
            operation.set_demand(demand)

    def get_service(self, service_name_to_search_for: str) -> Service:
        """
        Searches for the Service-Object with the given name out of the generic model.
        """
        for service_name in self.model.services.keys():
            if service_name == service_name_to_search_for:
                return self.model.services[service_name]

    def get_operation(self, operation_name_to_search_for: str, service: Service) -> Operation:
        """
        Searches for the Operation-Object in the given service.
        """
        for operation_name in service.operations.keys():
            if operation_name_to_search_for == operation_name:
                return service.operations[operation_name]

    def print_help_for_installing_librede(self):
        print("You have to manually install (build) LibReDE yourself (else its not runnable from console).")
        print("    1. Clone their repository")
        print("    2. Stay at the master branch (or go to commit \"f16c2c1\", depends whether they updated their repository)")
        print("    3. Call \"mvn clean install -DskipTests\" in the folder \"tools.descartes.librede.releng\"")
        print("    4. Come back here and type the path to the repository")

    def print_summary_if_user_wants(self):
        """
        Prints a string summarising the call of librede. (Only if the user wants to see it)
        """
        user_wants_output = get_valid_yes_no_input("Do you want a printed (console) summary of your use of LibReDE?")
        if user_wants_output:
            self.librede_input_creator.print_summary_of_input()
            self.librede_output_parser.print_final_results()
