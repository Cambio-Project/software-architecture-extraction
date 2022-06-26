import os
import pathlib
import shutil

from extractor.arch_models.model import IModel
from extractor.arch_models.operation import Operation
from extractor.arch_models.service import Service
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation
from extractor.r_d_e.librede_input_creator import LibredeInputCreator
from extractor.r_d_e.librede_output_parser import LibredeOutputParser


# Asks for the path of the LibReDE-installation.
# Creates the input-Files for LibReDE: response-times-.csv-Files, cpu-utilization-.csv-Files and the LibReDE_configuration-File.
# Calls LibReDE.
# Extracts the necessary information out of the output of LibReDE.
# Adds the demands in the generic model.
def calculate_and_add_demands_with_librede(model: IModel):
    print("Start calculating resource-demands...")
    path_to_librede_installation: str = input("Path to your LibReDE-installation (e.g. \"C:\\Users\\Max\\Downloads\\librede\"): ")
    path_to_librede_bat_file: str = path_to_librede_installation + "\\tools.descartes.librede.releng.standalone\\target\\standalone\\console\\"

    path_to_librede_files: str = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
    librede_input_creator = LibredeInputCreator(model, path_to_librede_files)
    print("\nExtracted information:")
    print(librede_input_creator)

    old_dir = os.getcwd()
    os.chdir(path_to_librede_bat_file)
    shutil.copy(librede_input_creator.get_path_to_configuration_file(), path_to_librede_bat_file)
    command: str = "librede.bat" + " -c \"" + librede_input_creator.configuration.get_file_name() + "\""
    print("Run <--" + command + "-->")
    os.system(command)
    os.remove(path_to_librede_bat_file + librede_input_creator.configuration.get_file_name())
    os.chdir(old_dir)

    librede_output_parser = LibredeOutputParser(librede_input_creator.operations_on_host, path_to_librede_files + "output\\")
    results_of_librede: dict[LibredeServiceOperation, float] = librede_output_parser.get_results_of_librede()
    for service_operation in results_of_librede.keys():
        add_demand_to_operation(service_operation, results_of_librede[service_operation])


# Sets the demand of the given operation.
def add_demand_to_operation(librede_service_operation: LibredeServiceOperation, demanded_utilization: float):
    service: Service = librede_service_operation.service
    operation: Operation = get_operation(librede_service_operation.operation_name, service)
    demand = int(demanded_utilization * service.capacity)
    operation.set_demand(demand)


# Searches for the Operation object in the service.
def get_operation(operation_name_to_look_for: str, service: Service) -> Operation:
    for operation_name in service.operations.keys():
        if operation_name_to_look_for == operation_name:
            return service.operations[operation_name]
