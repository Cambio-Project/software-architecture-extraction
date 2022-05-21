import json
from os.path import exists

from source.extractor.controllers.jaeger_network_manager import JaegerNetworkManager


# Class which forces the user putting in traces via the command line when instantiated.
#
# The input consists of two parts: type of traces and traces themselves.
# (Traces from jaeger can be fetched via the Jaeger HTTP API)
# Traces a retrievable through get_trace_list()
class InteractiveTraceInput:

    def __init__(self):
        self.traces_are_jaeger = False
        self.traces_are_zipkin = False
        self.use_jaeger_network = False
        self.traces = {'data': []}
        self.contains_multiple_traces = False

        self.ask_for_trace_type()
        if self.traces_are_jaeger:
            self.ask_for_use_of_jaeger_network()
        if self.use_jaeger_network:
            jaeger_network_manager = JaegerNetworkManager()
            self.traces = jaeger_network_manager.get_traces()
        else:
            self.ask_for_traces()
        self.contains_multiple_traces = len(self.get_trace_list()) > 1

    def ask_for_trace_type(self):
        trace_input_type = input("Your traces are from Jaeger or Zipkin? <j> or <z>: ")
        if trace_input_type == "j":
            self.traces_are_jaeger = True
        elif trace_input_type == "z":
            self.traces_are_zipkin = True
        else:
            pass  # TODO type of trace not supported

    def ask_for_use_of_jaeger_network(self):
        should_use_jaeger_network = input("Do you want to directly import your traces from the Jaeger Network API? <y> or <n>: ")
        self.use_jaeger_network = True if should_use_jaeger_network == "y" else False

    # Asks the user for trace locations and adds the content of each trace file to self.traces['data'].
    # The user can put in any number of traces, but at least one.
    def ask_for_traces(self):
        trace_file_path_input = input("First path to a " + self.get_trace_type() + "-trace file: ")
        while trace_file_path_input != "":
            self.add_trace_if_exists(trace_file_path_input)
            trace_file_path_input = input("Another path to a " + self.get_trace_type() + "-trace file [just enter to finish]: ")
        if len(self.traces['data']) == 0:
            pass  # TODO need at least one trace

    # Adds the file at the given path as a trace to self.traces. If the trace doesn't exist and error is printed.
    def add_trace_if_exists(self, trace_file_path):
        if exists(trace_file_path):
            trace_file_handler = open(trace_file_path, "r");
            trace_file_as_json = json.loads(trace_file_handler.read())
            self.traces['data'].append(trace_file_as_json['data'][0])
            trace_file_handler.close()
        else:
            print("File <" + trace_file_path + "> doesn't exist!\n")

    # Returns the list of traces which were put in at instantiation.
    def get_trace_list(self):
        return self.traces['data']

    def get_trace_type(self):
        if self.traces_are_jaeger:
            return "Jaeger"
        elif self.traces_are_zipkin:
            return "Zipkin"
        else:
            pass  # TODO error need at least one type of trace

    def __str__(self):
        number_of_traces = len(self.traces['data'])
        output_string = "Use " + str(number_of_traces) + " " + self.get_trace_type() + " traces "
        output_string += ("from the HTTP Jaeger API." if self.use_jaeger_network else "which were manually put in.")
        return output_string


def main():
    trace_input = InteractiveTraceInput()
    print("\nRegistered trace-input:")
    print(trace_input)


if __name__ == "__main__":
    main()
