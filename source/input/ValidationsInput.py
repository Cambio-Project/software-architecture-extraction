# class which forces the input of whether to validate the model and/or the
# architecture from the command line when instantiated
class ValidationsInput:
    def __init__(self):
        self.should_validate_model = False
        self.should_validate_architecture = False
        self.ask_for_validations()

    def ask_for_validations(self):
        validate_model_answer = input("Do you want a validation of the MODEL? <y> or <n>:")
        validate_architecture_answer = input("Do you want a validation of the ARCHITECTURE? <y> or <n>:")
        self.should_validate_model = True if validate_model_answer == "y" else False
        self.should_validate_architecture = True if validate_architecture_answer == "y" else False

    def __str__(self):
        return "validate model: " + str(self.should_validate_model) + ", validate architecture: " + str(
            self.should_validate_architecture)
