# class which forces the user typing the input for the extractor via the command line when instantiated
# the input consists of three parts: type of model to create, type of traces and traces themselves
class ExtractorInput:

    def __init__(self):
        self.should_create_resirio_model = False
        self.should_create_misim_model = False
        self.traces_are_jaeger = False
        self.traces_are_zipkin = False
        self.trace_file_locations = []

        self.ask_for_model_output_type()
        self.ask_for_trace_input_type()
        self.ask_for_traces()

    def ask_for_model_output_type(self):
        model_type_for_extraction = input("Create Model for Resirio [r] or MiSim [m]? ")
        if model_type_for_extraction == "r":
            self.should_create_resirio_model = True
        elif model_type_for_extraction == "m":
            self.should_create_misim_model = True
        else:
            pass  # TODO type of output model not supported

    def ask_for_trace_input_type(self):
        trace_input_type = input("Your traces are from Jaeger [j] or Zipkin [z]? ")
        if trace_input_type == "j":
            self.traces_are_jaeger = True
        elif trace_input_type == "z":
            self.traces_are_zipkin = True
        else:
            pass  # TODO type of trace not supported

    # asks the user via the command line for trace locations
    # the user can add any number of trace-files
    def ask_for_traces(self):
        trace_file_input = input("First trace file location: ")
        if trace_file_input == "":
            pass  # TODO need at least one trace
        while trace_file_input != "":
            self.trace_file_locations.append(trace_file_input)
            trace_file_input = input("Another trace file [just enter to finish]: ")

    def __str__(self):
        output_string = "Creates a model for " + ("Resirio" if self.should_create_resirio_model else "MiSim")
        output_string += " with " + ("Jaeger" if self.traces_are_jaeger else "Zipkin") + " traces.\n"
        output_string += "Traces: " + str(self.trace_file_locations)
        return output_string
