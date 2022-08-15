import json
import os.path
from os.path import exists
from input.input_utils import get_valid_dir_path_input, get_valid_int_input, get_valid_string_input_with_finite_valid_options, get_valid_yes_no_input, get_valid_file_path_input, get_valid_string_input_with_predicates

from extractor.controllers.jaeger_network_manager import JaegerNetworkManager
from extractor.controllers.zipkin_network_manager import ZipkinNetworkManager


class InteractiveTraceInput:
    """
    Class which forces the user putting in traces via the command line when instantiated.
    The input consists of two parts: type of traces and traces themselves.
    """

    def __init__(self):
        self.traces_are_jaeger = False
        self.traces_are_zipkin = False
        self.traces_are_open_x_trace = False
        self.use_jaeger_network = False
        self.use_zipkin_network = False
        self.traces = None
        self.create_api_backup = False
        self.load_jaeger_backup = False
        self.ask_for_trace_inputs()

    def ask_for_trace_inputs(self):
        self.ask_for_trace_type()
        if self.traces_are_jaeger:
            self.ask_for_use_of_jaeger_network()
        elif self.traces_are_zipkin:
            self.ask_for_use_of_zipkin_network()

        if self.use_jaeger_network:
            jaeger_network_manager = JaegerNetworkManager()
            self.traces = jaeger_network_manager.get_traces()
            if self.create_api_backup:
                jaeger_network_manager.create_backup()
        elif self.use_zipkin_network:
            zipkin_network_manager = ZipkinNetworkManager()
            limit = get_valid_int_input("Please enter a limit how many traces you wish to retrieve: ")
            self.traces = zipkin_network_manager.get_traces(int(limit))
            if self.create_api_backup:
                zipkin_network_manager.create_backup(int(limit))
        elif self.load_jaeger_backup:
            jaeger_network_manager = JaegerNetworkManager()
            path = get_valid_dir_path_input("Please enter the path to the folder which contains the backup: ")
            self.traces = jaeger_network_manager.load_backup(path)
        else:
            self.ask_for_traces_via_command_line()

    def ask_for_trace_type(self):
        trace_input_type = get_valid_string_input_with_finite_valid_options("Do you want to enter Jaeger, Zipkin or Open.xtrace traces?", ["j", "z", "o"])
        self.traces_are_jaeger = trace_input_type == "j"
        self.traces_are_zipkin = trace_input_type == "z"
        self.traces_are_open_x_trace = trace_input_type == "o"

    def ask_for_use_of_jaeger_network(self):
        should_use_jaeger_network = get_valid_string_input_with_finite_valid_options("Do you want to directly import your traces from the Jaeger HTTP API or use a previously created backup?", ["y", "n", "b"])
        if should_use_jaeger_network == "y":
            self.create_api_backup = get_valid_yes_no_input("Do you wish to create a backup of the traces?")
        self.use_jaeger_network = True if should_use_jaeger_network == "y" else False
        self.load_jaeger_backup = True if should_use_jaeger_network == "b" else False

    def ask_for_use_of_zipkin_network(self):
        should_use_zipkin_network = get_valid_yes_no_input("Do you want to directly import your traces from the Zipkin HTTP API?")
        if should_use_zipkin_network:
            self.create_api_backup = get_valid_yes_no_input("Do you wish to create a backup of the traces?")
        self.use_zipkin_network = True if should_use_zipkin_network else False

    def ask_for_traces_via_command_line(self):
        """
        Asks the user for trace locations and adds the content of each trace file to self.traces.
        The user can put in any number of traces.
        """
        self.traces = {'data': []} if self.traces_are_jaeger else []
        trace_file_path_input: str = get_valid_file_path_input("Path to a " + self.get_trace_type() + "-trace file.")
        self.add_trace(trace_file_path_input)
        while True:
            trace_file_path_input: str = get_valid_string_input_with_predicates("Path to a " + self.get_trace_type() + "-trace file.", ["Path", "Enter to stop"], [lambda a: os.path.isfile(a), lambda a: a == ""])[1]
            if trace_file_path_input != "":
                self.add_trace(trace_file_path_input)
            else:
                break

    def add_trace(self, trace_file_path):
        """
        Adds the trace of the given file to self.traces.
        """
        trace_file_handler = open(trace_file_path, "r")
        trace_file_as_json = json.loads(trace_file_handler.read())
        input_trace_list = trace_file_as_json["data"] if self.traces_are_jaeger else trace_file_as_json
        if self.traces_are_jaeger or self.traces_are_open_x_trace:
            for single_trace in input_trace_list:
                self.get_list_of_traces().append(single_trace)
        elif self.traces_are_zipkin:
            if isinstance(trace_file_as_json[0], list):
                for trace_list in trace_file_as_json:
                    self.get_list_of_traces().append(trace_list)
            else:
                self.get_list_of_traces().append(trace_file_as_json)
        trace_file_handler.close()

    def get_list_of_traces(self):
        return self.traces["data"] if self.traces_are_jaeger else self.traces

    def get_traces(self):
        return self.traces

    def get_trace_type(self):
        if self.traces_are_jaeger:
            return "Jaeger"
        elif self.traces_are_zipkin:
            return "Zipkin"
        elif self.traces_are_open_x_trace:
            return "OpenXTrace"

    def get_number_of_traces(self):
        return len(self.get_list_of_traces())

    def print_summary_of_trace_input(self):
        print("Use " + str(self.get_number_of_traces()) + " " + self.get_trace_type() + "-Traces; ", end="")
        print("Input-method: " + ("HTTP-Network" if self.use_jaeger_network or self.use_zipkin_network else "Manual"))
