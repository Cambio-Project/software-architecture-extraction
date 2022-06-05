import json

from extractor.r_d_e.LibReDE_CSV_Creator import LibReDE_CSV_Creator

trace = json.loads(open("trace_stub.json", "r").read())
csv_creator = LibReDE_CSV_Creator(trace)
print(csv_creator)
