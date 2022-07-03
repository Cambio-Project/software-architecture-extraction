import json
from os.path import exists

from extractor.controllers.jaeger_network_manager import JaegerNetworkManager
from extractor.controllers.zipkin_network_manager import ZipkinNetworkManager


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
        self.use_zipkin_network = False
        self.traces = None
        self.contains_multiple_traces = False

        self.ask_for_trace_type()
        if self.traces_are_jaeger:
            self.ask_for_use_of_jaeger_network()
        elif self.traces_are_zipkin:
            self.ask_for_use_of_zipkin_network()

        if self.use_jaeger_network:
            jaeger_network_manager = JaegerNetworkManager()
            self.traces = jaeger_network_manager.get_traces()
        elif self.use_zipkin_network:
            zipkin_network_manager = ZipkinNetworkManager()
            limit = input("Please enter a limit (integer) how many traces you wish to retrieve: ")
            self.traces = zipkin_network_manager.get_traces(int(limit))
        else:
            self.ask_for_traces()

    def ask_for_trace_type(self):
        trace_input_type = input("Your traces are from Jaeger or Zipkin? <j> or <z>: ")
        if trace_input_type == "j":
            self.traces_are_jaeger = True
        elif trace_input_type == "z":
            self.traces_are_zipkin = True
        else:
            print("Trace-Type <" + trace_input_type + "> is not supported, try another...\n")
            self.ask_for_trace_type()

    def ask_for_use_of_jaeger_network(self):
        should_use_jaeger_network = input(
            "Do you want to directly import your traces from the Jaeger HTTP API? <y> or <n>: ")
        self.use_jaeger_network = True if should_use_jaeger_network == "y" else False

    def ask_for_use_of_zipkin_network(self):
        should_use_zipkin_network = input(
            "Do you want to directly import your traces from the Zipkin HTTP API? <y> or <n>: ")
        self.use_zipkin_network = True if should_use_zipkin_network == "y" else False

    # Asks the user for trace locations and adds the content of each trace file to self.traces['data'].
    # The user can put in any number of traces, but at least one.
    def ask_for_traces(self):
        trace_file_path_input: str = input("Path to your " + self.get_trace_type() + "-trace file: ")
        user_gave_a_valid_trace: bool = self.set_trace_if_exists(trace_file_path_input)
        while not user_gave_a_valid_trace:
            trace_file_path_input: str = input("Path to your " + self.get_trace_type() + "-trace file: ")
            user_gave_a_valid_trace: bool = self.set_trace_if_exists(trace_file_path_input)
        cli_input = None
        if self.traces_are_jaeger:
            cli_input = self.traces['data']
        elif self.traces_are_zipkin:
            cli_input = self.traces

        if len(cli_input) == 0:
            pass  # TODO need at least one trace

    # Adds the file at the given path as a trace to self.traces. If the trace doesn't exist and error is printed.
    def set_trace_if_exists(self, trace_file_path):
        if exists(trace_file_path):
            trace_file_handler = open(trace_file_path, "r")
            trace_file_as_json = json.loads(trace_file_handler.read())
            self.traces = trace_file_as_json
            self.contains_multiple_traces = len(trace_file_as_json) > 1
            trace_file_handler.close()
            return True
        else:
            print("File <" + trace_file_path + "> doesn't exist!\n")
            return False

    def get_trace_type(self):
        if self.traces_are_jaeger:
            return "Jaeger"
        elif self.traces_are_zipkin:
            return "Zipkin"

    # Calculates the number of traces which were put in at instantiation.
    def get_number_of_traces(self):
        if self.traces_are_jaeger:
            return len(self.traces['data'])
        elif self.traces_are_zipkin:
            return len(self.traces)

    # Returns the variable containing all traces which were put in at instantiation.
    def get_traces(self):
        if self.traces_are_jaeger:
            return self.traces["data"]
        elif self.traces_are_zipkin:
            return self.traces

    def __str__(self):
        output_string = "Use " + str(self.get_number_of_traces()) + " " + self.get_trace_type() + "-Traces.\n"
        output_string += "Input-method: " + (
            "HTTP-Network" if self.use_jaeger_network or self.use_zipkin_network else "Manual") + "."
        return output_string


def manual_input_test():
    trace_input = InteractiveTraceInput()
    print("\nRegistered trace-input:")
    print(trace_input)


if __name__ == "__main__":
    manual_input_test()
