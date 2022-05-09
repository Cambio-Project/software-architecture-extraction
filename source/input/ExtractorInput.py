# class which forces the input of a transformation model from the command line when instantiated
class ExtractorInput:

    def __init__(self):
        self.should_create_resirio_model = False
        self.should_create_misim_model = False
        self.traces_are_jaeger = False
        self.traces_are_zipkin = False
        self.trace_file_locations = []

        self.set_types()
        self.add_traces()

    def set_types(self):
        model_type_for_extraction = input("Extract Model for Resirio [r] or MiSim [m]? ")
        if model_type_for_extraction == "r":
            self.should_create_resirio_model = True
        elif model_type_for_extraction == "m":
            self.should_create_misim_model = True
        else:
            pass  # error
        trace_input_type = input("Traces for input are from Jaeger [j] or Zipkin [z]? ")
        if trace_input_type == "j":
            self.traces_are_jaeger = True
        elif trace_input_type == "z":
            self.traces_are_zipkin = True
        else:
            pass  # error

    def add_traces(self):
        trace_file_input = input("Trace file location: ")
        while trace_file_input != "":
            self.trace_file_locations.append(trace_file_input)
            trace_file_input = input("Another trace file [just enter to finish]: ")

    def __str__(self):
        output_string = "Creates a model for " + ("Resirio" if self.should_create_resirio_model else "MiSim")
        output_string += " with " + ("Jaeger" if self.traces_are_jaeger else "Zipkin") + " traces.\n"
        output_string += "Traces: " + str(self.trace_file_locations)
        return output_string
