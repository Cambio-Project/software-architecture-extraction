# Class which forces the user to type the input of the settings via the command line when instantiated.
# The input consists of three parts: Analyses, Validation and Export.
class InteractiveSettingsInput:

    def __init__(self):
        self.should_analyse_model = False
        self.should_analyse_architecture = False

        self.should_validate_model = False
        self.should_validate_architecture = False

        self.should_export_model = False
        self.should_export_architecture = False
        self.should_be_lightweight_export = False

        self.ask_for_analyses()
        print()
        self.ask_for_validations()
        print()
        self.ask_for_exports()

    def ask_for_analyses(self):
        analyse_model_answer = input("Do you want an analyses of the MODEL? <y> or <n>: ")
        analyse_architecture_answer = input("Do you want an analyses of the ARCHITECTURE? <y> or <n>: ")
        self.should_analyse_model = True if analyse_model_answer == "y" else False
        self.should_analyse_architecture = True if analyse_architecture_answer == "y" else False

    def ask_for_validations(self):
        validate_model_answer = input("Do you want a validation of the MODEL? <y> or <n>: ")
        validate_architecture_answer = input("Do you want a validation of the ARCHITECTURE? <y> or <n>: ")
        self.should_validate_model = True if validate_model_answer == "y" else False
        self.should_validate_architecture = True if validate_architecture_answer == "y" else False

    def ask_for_exports(self):
        should_export_model_answer = input("Do you want to export the MODEL? <y> or <n>: ")
        should_export_architecture_answer = input("Do you want to export the ARCHITECTURE? <y> or <n>: ")
        should_be_lightweight_answer = input("Do you want the export of the graph being lightweight? <y> or <n>: ")
        self.should_export_model = True if should_export_model_answer == "y" else False
        self.should_export_architecture = True if should_export_architecture_answer == "y" else False
        self.should_be_lightweight_export = True if should_be_lightweight_answer == "y" else False

    def __str__(self):
        output_string = "Analyse Model: " + str(self.should_analyse_model) + ", Analyse Architecture: " + str(
            self.should_analyse_architecture)
        output_string += "\nValidate Model: " + str(self.should_validate_model) + ", Validate Architecture: " + str(
            self.should_validate_architecture)
        output_string += "\nExport Model: " + str(self.should_export_model) + ", Export Architecture: " + str(
            self.should_export_architecture) + ", Lightweight export: " + str(self.should_be_lightweight_export)
        return output_string


def main():
    settings_input = InteractiveSettingsInput()
    print("\nRegistered Settings:")
    print(settings_input)


if __name__ == "__main__":
    main()
