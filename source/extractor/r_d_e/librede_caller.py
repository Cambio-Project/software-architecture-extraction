import os
import pathlib

from extractor.r_d_e.librede_input_creator import LibReDE_Input_Creator


def call_librede(trace) -> dict[str, int]:
    path_to_librede_installation: str = input("Path to your LibReDE-installation (Example: C:\\Users\\Max\\librede\\): ")
    librede_bat_file = path_to_librede_installation + "\\tools.descartes.librede.releng.standalone\\target\\standalone\\console\\librede.bat"
    output_path: str = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    librede_input_creator = LibReDE_Input_Creator(trace, output_path)
    print("Extracted information out of trace:")
    print(librede_input_creator)
    full_command = librede_bat_file + " -c \"" + librede_input_creator.get_path_to_configuration_file() + "\""
    os.system(full_command)
    return None
