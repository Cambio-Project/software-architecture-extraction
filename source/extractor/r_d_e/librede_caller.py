import os
import pathlib
import shutil

from extractor.arch_models.model import IModel
from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service
from extractor.r_d_e.librede_input_creator import LibredeInputCreator
from extractor.r_d_e.librede_output_parser import LibredeOutputParser


class LibredeCaller:
    """
    Class which contains the functionality to extract the input for LibReDE out of a generic model, call LibReDE,
    parse its output and write the gained information back in the generic model (to the field "demand" of an operation).
    All of this automatically happens at instantiation.
    """

    relative_path_to_librede_bat_file = "\\tools.descartes.librede.releng.standalone\\target\\standalone\\console\\"
    approaches = ["ResponseTimeApproximationApproach", "ServiceDemandLawApproach", "WangKalmanFilterApproach"]

    def __init__(self, model: IModel):
        self.model: IModel = model
        self.path_to_librede_files = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
        self.librede_input_creator: LibredeInputCreator = LibredeInputCreator(self.model, self.path_to_librede_files, self.approaches)
        self.path_to_librede_bat_file: str = self.ask_for_path_of_librede_installation() + self.relative_path_to_librede_bat_file
        self.call_librede()
        self.librede_output_parser = LibredeOutputParser(self.librede_input_creator.operations_on_host, self.path_to_librede_files + "output\\", self.approaches)
        self.parse_output_of_librede()

    def ask_for_path_of_librede_installation(self):
        """
        Asks for a path to the cloned librede repository (must already had been builded).
        By typing "help", a helpful message is printed about how to install LibReDE.
        Asks for a path recursively, till a valid path is put in.
        """
        answer_of_user: str = input("Path to your LibReDE-installation (e.g. \"C:\\Users\\Max\\Downloads\\librede\") [type <help>, for how to install]: ")
        if answer_of_user == "help":
            self.print_help_for_installing_librede()
            return self.ask_for_path_of_librede_installation()
        else:
            path_to_librede_installation = answer_of_user
            if not os.path.exists(path_to_librede_installation + self.relative_path_to_librede_bat_file):
                print("LibReDE-installation at <" + path_to_librede_installation + self.relative_path_to_librede_bat_file + "> couldn't be found, please try again.\n")
                return self.ask_for_path_of_librede_installation()
            else:
                return path_to_librede_installation

    def call_librede(self):
        """
        Calls LibReDE.
        LibReDE needs a workaround: The .bat needs to be called from the path where it is and the configurations must be in the same folder.
        That's why the current working directory is changed, later restored and the configuration file gets copied to the location of the
        .bat and then deleted.
        """
        old_dir = os.getcwd()
        for configuration in self.librede_input_creator.configurations:
            shutil.copy(configuration.get_path_to_configuration_file(), self.path_to_librede_bat_file)
        os.chdir(self.path_to_librede_bat_file)
        for configuration in self.librede_input_creator.configurations:
            command: str = "librede.bat" + " -c " + configuration.get_file_name() + ""
            print("Running \"" + command + "\" for operation \"" + configuration.service_operation.operation_name + "\" on host \"" + configuration.service_operation.host.name + "\"")
            os.system(command)
            os.remove(self.path_to_librede_bat_file + configuration.get_file_name())
        os.chdir(old_dir)

    def parse_output_of_librede(self):
        """
        Extracts the necessary information out of the output of LibReDE and adds the demands in the generic model.
        """
        results_of_librede: dict[tuple[str, str], float] = self.librede_output_parser.get_results_of_librede()
        for service_name, operation_name in results_of_librede.keys():
            self.add_demand_to_operation(service_name, operation_name, results_of_librede[(service_name, operation_name)])

    def add_demand_to_operation(self, service_name, operation_name, demanded_utilization: float):
        """
        Sets the demand of an operation of a service by multiplying the estimated utilization with the capacity of the service.
        """
        service: Service = self.get_service(service_name)
        operation: Operation = self.get_operation(operation_name, service)
        demand = int(demanded_utilization * service.capacity)
        operation.set_demand(demand)

    def get_service(self, service_name) -> Service:
        """
        Searches for the Service-Object with the given name out of the generic model.
        """
        for service in self.model.services.keys():
            if service == service_name:
                return self.model.services[service]

    def get_operation(self, operation_name_to_look_for: str, service: Service) -> Operation:
        """
        Searches for the Operation-Object in the service.
        """
        for operation_name in service.operations.keys():
            if operation_name_to_look_for == operation_name:
                return service.operations[operation_name]

    def print_help_for_installing_librede(self):
        print("-------------------------------------------------")
        print("You have to manually install/build LibReDE (else its not runnable from console).")
        print("  1. Clone their repository")
        print("  2. Stay at the master branch (or go to commit \"f16c2c1\", depends whether they updated their repository)")
        print("  3. Call <mvn clean install -DskipTests> in the folder \"tools.descartes.librede.releng\"")
        print("  4. Come back here and type the path to the repository")
        print("-------------------------------------------------")

    def print_summary(self):
        """
        Prints a string summarising the call of librede
        """
        print("LibReDE-Summary:")
        print("------------------------------------------")
        print("Input:")
        print(self.librede_input_creator)
        print("Output:")
        print(self.librede_output_parser.get_final_results_as_str(), end="")
        print("------------------------------------------")
