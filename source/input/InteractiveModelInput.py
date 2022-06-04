# Class which forces the input of a either a resirio- or misim-model or the information of no model
class InteractiveModelInput:

    def __init__(self):
        self.contains_resirio_model = False
        self.contains_misim_model = False
        self.contains_misim_experimental_model = False
        self.model_file_path = None
        self.experimental_misim_model_file_path = None
        self.ask_for_model_types()
        if self.contains_model():
            self.ask_for_model_files()

    def ask_for_model_types(self):
        model_answer = input("Do you want to put in a previously created RESIRIO-/MiSim-model or no model? <r>, <m> or <n>: ")
        if model_answer == "r":
            self.contains_resirio_model = True
        elif model_answer == "m":
            self.contains_misim_model = True
            experimental_misim_model_answer = input("Do you want to put in an misim experimental model? <y> or <n>: ")
            self.contains_misim_experimental_model = True if experimental_misim_model_answer == "y" else False
        elif model_answer == "n":
            pass
        else:
            pass  # TODO invalid answer

    def ask_for_model_files(self):
        self.model_file_path = input(("RESIRIO" if self.contains_resirio_model else "MiSim") + "-model filepath: ")
        if self.contains_misim_experimental_model:
            self.experimental_misim_model_file_path = input("Experimental Misim-model filepath: ")
        if self.model_file_path == "" or self.experimental_misim_model_file_path == "":
            pass  # TODO invalid model file path

    def contains_model(self):
        return self.contains_resirio_model or self.contains_misim_model

    def get_model_file_path(self):
        return self.model_file_path

    def __str__(self):
        if self.contains_model():
            output = ("RESIRIO" if self.contains_resirio_model else "MiSim") + "-model at <" + self.model_file_path + ">"
            output += "\nExperimental MiSim-model at <" + self.experimental_misim_model_file_path + ">" if self.contains_misim_experimental_model else ""
            return output
        else:
            return "No model."


def manual_input_test():
    model_input = InteractiveModelInput()
    print("\nRegistered Model:")
    print(model_input)


if __name__ == "__main__":
    manual_input_test()
