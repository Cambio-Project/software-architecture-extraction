from source.extractor.controllers.jaeger_network_manager import JaegerNetworkManager


# Class which forces the user typing the input for MiSim via the command line when instantiated.
# The input consists of three parts: type of traces and traces themselves (traces from jaeger can be manually typed
# or fetched via the Jaeger HTTP API.
class InteractiveExtractorInput:

    def __init__(self):
        self.traces_are_jaeger = False
        self.traces_are_zipkin = False
        self.use_jaeger_network = False
        self.traces = {'data': []}

        self.ask_for_trace_type()
        if self.traces_are_jaeger:
            self.ask_for_use_of_jaeger_network()

        if not self.use_jaeger_network:
            self.ask_for_traces()
        else:
            jaeger_network_manager = JaegerNetworkManager()
            self.traces = jaeger_network_manager.get_traces()

    def ask_for_trace_type(self):
        trace_input_type = input("Your traces are from Jaeger or Zipkin? <j> or <z>:")
        if trace_input_type == "j":
            self.traces_are_jaeger = True
        elif trace_input_type == "z":
            self.traces_are_zipkin = True
        else:
            pass  # TODO type of trace not supported

    def ask_for_use_of_jaeger_network(self):
        use_jaeger_network_answer = input(
            "Do you want to directly import your traces from the Jaeger Network API? <y> or <n>:")
        if use_jaeger_network_answer == "y":
            self.use_jaeger_network = True
        elif use_jaeger_network_answer == "n":
            self.use_jaeger_network = False
        else:
            pass  # TODO invalid answer

    # Asks the user for trace locations and adds the content of each trace file to self.traces['data'].
    # The user can put in any number of traces, but at least one.
    def ask_for_traces(self):
        trace_file_path_input = input("First path to a trace file: ")
        if trace_file_path_input == "":
            pass  # TODO need at least one trace
        while trace_file_path_input != "":
            trace_file_content = open(trace_file_path_input, "r");
            self.traces['data'].append(trace_file_content.read())
            trace_file_content.close()
            trace_file_path_input = input("Another path to a trace file [just enter to finish]: ")

    # Returns the list of traces which were put in.
    def get_trace_list(self):
        return self.traces['data']

    def __str__(self):
        number_of_traces = len(self.traces['data'])
        output_string = "Create MiSim-Model out of " + str(number_of_traces) + " traces of type " + (
            "Jaeger" if self.traces_are_jaeger else "Zipkin") + "."
        output_string += "\nThey were fetched from the Jaeger HTTP API" if self.use_jaeger_network else ""
        return output_string
