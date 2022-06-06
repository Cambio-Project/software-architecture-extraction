import json
import os
import pathlib

from extractor.r_d_e.librede_input_creator import LibReDE_Input_Creator

trace = json.loads(open("trace_stub.json", "r").read())
output_path: str = str(pathlib.Path(__file__).parent.resolve()) + "\\librede_files\\"
if not os.path.exists(output_path):
    os.mkdir(output_path)
csv_creator = LibReDE_Input_Creator(trace, output_path)
print(csv_creator)
