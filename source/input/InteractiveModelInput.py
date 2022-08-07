import os.path

from input.input_utils import get_valid_string_input_with_finite_valid_options_and_descriptions, \
    get_valid_file_path_input, get_valid_string_input_with_predicates


class InteractiveModelInput:
    """
    Class which forces the input of either a RESIRIO- or MiSim-model or the information of no model
    """

    def __init__(self):
        self.contains_generic_model = False
        self.contains_misim_model = False
        self.model_file_path = None
        self.ask_for_model()

    def ask_for_model(self):
        input_specification = "Optionally enter a previosuly created extraction:"
        input_descriptions = [
            "Path to extraction (either .dat-file for Generic Model (pickle) or .json for MiSim-architecture",
            "Enter for no model"]
        inputs_predicates = [os.path.isfile, lambda a: a == ""]
        model_answer = get_valid_string_input_with_predicates(input_specification, input_descriptions,
                                                              inputs_predicates)
        if model_answer[0] == 0:
            self.model_file_path = model_answer[1]
            self.contains_generic_model = model_answer[1].endswith(".dat")
            self.contains_misim_model = model_answer[1].endswith(".json")

    def contains_model(self):
        return self.contains_generic_model or self.contains_misim_model

    def get_model_file_path(self):
        return self.model_file_path

    def print_summary_of_model_input(self):
        print("Model-input: ", end="")
        if self.contains_model():
            print(
                ("Generic" if self.contains_generic_model else "MiSim") + "-model at \"" + self.model_file_path + "\"")
        else:
            print("No model.")
