import os
import pathlib
import shutil

from extractor.arch_models.model import IModel
from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation
from extractor.r_d_e.librede_input_creator import LibredeInputCreator
from extractor.r_d_e.librede_output_parser import LibredeOutputParser


class LibredeCaller:
    """
    Class which contains the functionality to extract the input for LibReDE out of a generic model, call LibReDE,
    parse its output and write the gained information back in the generic model (to the field "demand" of an operation).
    All of this automatically happens at instantiation.
    """

    def __init__(self, model: IModel):
        self.model: IModel = model
        self.path_to_librede_files = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
        self.librede_input: LibredeInputCreator = self.create_input_for_librede()
        self.path_to_librede_bat_file: str = self.ask_for_path_of_librede_bat_file()
        self.call_librede()
        self.parse_output_of_librede()

    # Creates the input-Files for LibReDE: response-times-.csv-Files, cpu-utilization-.csv-Files and the LibReDE_configuration-File.
    def create_input_for_librede(self) -> LibredeInputCreator:
        return LibredeInputCreator(self.model, self.path_to_librede_files)

    # Asks for the path of the LibReDE-installation. Helps the user with their LibReDE installation, if needed.
    def ask_for_path_of_librede_bat_file(self):
        answer_of_user: str = input("Path to your LibReDE-installation (e.g. \"C:\\Users\\Max\\Downloads\\librede\") [type <help>, for how to install]: ")
        if answer_of_user == "help":
            path_to_librede_installation = self.help_and_ask_for_librede_installation_path_again()
        else:
            path_to_librede_installation = answer_of_user
        return path_to_librede_installation + "\\tools.descartes.librede.releng.standalone\\target\\standalone\\console\\"

    # Calls LibReDE.
    # LibReDE needs a workaround: The .bat needs to be called from the location it is and the configuration must be in the same folder.
    # That's why the current working directory is changed and later restored and
    # the configuration file gets copied to the location of the .bat and then deleted.
    def call_librede(self):
        old_dir = os.getcwd()
        os.chdir(self.path_to_librede_bat_file)
        shutil.copy(self.librede_input.get_path_to_configuration_file(), self.path_to_librede_bat_file)
        command: str = "librede.bat" + " -c \"" + self.librede_input.configuration.get_file_name() + "\""
        print("Running <--" + command + "-->")
        os.system(command)
        os.remove(self.path_to_librede_bat_file + self.librede_input.configuration.get_file_name())
        os.chdir(old_dir)
        print("Finished call of LibReDE.")

    # Extracts the necessary information out of the output of LibReDE and adds the demands in the generic model.
    def parse_output_of_librede(self):
        librede_output_parser = LibredeOutputParser(self.librede_input.operations_on_host, self.path_to_librede_files + "output\\")
        results_of_librede: dict[tuple[str, str], float] = librede_output_parser.get_results_of_librede()
        for service_name, operation_name in results_of_librede.keys():
            self.add_demand_to_operation(service_name, operation_name, results_of_librede[(service_name, operation_name)])

    # Prints a help message for installing LibReDE and then asks for the path.
    def help_and_ask_for_librede_installation_path_again(self):
        print("-------------------------------------------------")
        print("You have to manually install/build LibReDE (else its not runnable from console).")
        print("  1. Clone their repository")
        print("  2. Stay at the master branch (or go to commit \"f16c2c1\", depends whether they updated their repository)")
        print("  3. Call <mvn clean install -DskipTests> in the folder \"tools.descartes.librede.releng\"")
        print("  4. Come back here and type the path to the repository")
        print("-------------------------------------------------")
        return input("Path to your LibReDE-installation (e.g. \"C:\\Users\\Max\\Downloads\\librede\"): ")

    # Sets the demand of the given operation.
    def add_demand_to_operation(self, service_name, operation_name, demanded_utilization: float):
        service: Service = self.get_service(service_name)
        operation: Operation = self.get_operation(operation_name, service)
        demand = int(demanded_utilization * service.capacity)
        operation.set_demand(demand)

    # Retrieves the Service-object with the given name out of the generic model.
    def get_service(self, service_name) -> Service:
        for service in self.model.services.keys():
            if service == service_name:
                return self.model.services[service]

    # Searches for the Operation object in the service.
    def get_operation(self, operation_name_to_look_for: str, service: Service) -> Operation:
        for operation_name in service.operations.keys():
            if operation_name_to_look_for == operation_name:
                return service.operations[operation_name]
