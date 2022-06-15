import os
import pathlib

from extractor.arch_models.model import IModel
from extractor.r_d_e.librede_input_creator import LibredeInputCreator
from extractor.r_d_e.librede_output_parser import LibReDE_Output_Parser


<<<<<<< HEAD
def call_librede(trace) -> dict[str, int]:
    # Determines the path to the LibReDE-installation
=======
# Asks for the path of the LibReDE-installation.
# Creates the input-Files for LibReDE: response-times-.csv-Files, cpu-utilization-.csv-Files and the LibReDE_configuration-File.
# Calls LibReDE.
# Extracts the necessary information out of the output of LibReDE.
# Returns a mapping between each operation (name) and its demand.
def call_librede(model: IModel) -> dict[str, int]:
>>>>>>> cfb79567ba16e29ff6dada8b0d02c0c3794cb699
    path_to_librede_installation: str = input("Path to your LibReDE-installation (e.g. \"C:\\Users\\Max\\Downloads\\librede\"): ")
    librede_bat_file: str = path_to_librede_installation + "\\tools.descartes.librede.releng.standalone\\target\\standalone\\console\\librede.bat"

    # Creates the input-Files for LibReDE: response-times-.csv-Files, cpu-utilization-.csv-Files and the LibReDE_configuration-File.
    path_to_librede_files: str = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
    librede_input_creator = LibredeInputCreator(model, path_to_librede_files)
    print("\nExtracted information:")
    print(librede_input_creator)

    # Calls LibReDE with the calculated input.
    full_command: str = librede_bat_file + " -c \"" + librede_input_creator.get_path_to_configuration_file() + "\""
    print("Run <--" + full_command + "-->")
    os.system(full_command)

<<<<<<< HEAD
    # Parses the output of LibReDE into a mapping between each operation (name) and its demand.
    librede_output_parser = LibReDE_Output_Parser(librede_input_creator.services, path_to_librede_files + "output\\")
=======
    librede_output_parser = LibReDE_Output_Parser(librede_input_creator.operations_on_host, path_to_librede_files + "output\\")
>>>>>>> cfb79567ba16e29ff6dada8b0d02c0c3794cb699
    return librede_output_parser.get_results_of_librede()
