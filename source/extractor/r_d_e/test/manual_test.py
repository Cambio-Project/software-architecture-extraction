import json

from extractor.r_d_e.librede_input_creator import LibReDE_Input_Creator

trace = json.loads(open("trace_stub.json", "r").read())
csv_creator = LibReDE_Input_Creator(trace)
print(csv_creator)
