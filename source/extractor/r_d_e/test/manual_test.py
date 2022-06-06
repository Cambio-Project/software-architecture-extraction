import json

from extractor.r_d_e.librede_caller import call_librede

trace = json.loads(open("trace_stub.json", "r").read())
call_librede(trace)
