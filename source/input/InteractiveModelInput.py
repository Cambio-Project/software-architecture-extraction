from input.input_utils import get_valid_string_input_with_finite_valid_options_and_descriptions, get_valid_file_path_input


class InteractiveModelInput:
    """
    Class which forces the input of either a RESIRIO- or MiSim-model or the information of no model
    """

    def __init__(self):
        self.contains_generic_model = False
        self.contains_misim_model = False
        self.ask_for_model_type()
        if self.contains_model():
            self.model_file_path = get_valid_file_path_input("Path to a " + ("Generic (Pickle) " if self.contains_generic_model else "MiSim") + "-model file")

    def ask_for_model_type(self):
        input_specification = "Do you want to enter a Generic model (Pickle) or MiSim model that has been created previously or no model?"
        input_descriptions = ["g", "m", "Enter for no model"]
        inputs = ["g", "m", ""]
        model_answer = get_valid_string_input_with_finite_valid_options_and_descriptions(input_specification, input_descriptions, inputs)
        self.contains_generic_model = model_answer == "g"
        self.contains_misim_model = model_answer == "m"

    def contains_model(self):
        return self.contains_generic_model or self.contains_misim_model

    def get_model_file_path(self):
        return self.model_file_path

    def print_summary_of_model_input(self):
        print("Model-input: ", end="")
        if self.contains_model():
            print(("Generic" if self.contains_generic_model else "MiSim") + "-model at \"" + self.model_file_path + "\"")
        else:
            print("No model.")
