import os
import pathlib

from extractor.r_d_e.librede_input_creator import LibReDE_InputCreator
from extractor.r_d_e.librede_output_parser import LibReDE_Output_Parser


# Asks for the path of the LibReDE-installation.
# Creates the input-Files for LibReDE: response-times-.csv-Files, cpu-utilization-.csv-Files and the LibReDE_configuration-File.
# Calls LibReDE.
# Extracts the necessary information out of the output of LibReDE.
# Returns a mapping between each operation (name) and its demand.
def call_librede(trace) -> dict[str, int]:
    path_to_librede_installation: str = input("Path to your LibReDE-installation (e.g. \"C:\\Users\\Max\\Downloads\\librede\"): ")
    librede_bat_file: str = path_to_librede_installation + "\\tools.descartes.librede.releng.standalone\\target\\standalone\\console\\librede.bat"

    path_to_librede_files: str = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
    librede_input_creator = LibReDE_InputCreator(trace, path_to_librede_files)
    print("\nExtracted information:")
    print(librede_input_creator)

    full_command: str = librede_bat_file + " -c \"" + librede_input_creator.get_path_to_configuration_file() + "\""
    print("Run <--" + full_command + "-->")
    os.system(full_command)

    librede_output_parser = LibReDE_Output_Parser(librede_input_creator.services, path_to_librede_files + "output\\")
    return librede_output_parser.get_results_of_librede()
