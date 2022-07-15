# Class which forces the user to type the input of the settings via the command line when instantiated.
# The input consists of three parts: Analyses, Validation and Export.
class InteractiveSettingsInput:

    def __init__(self):
        self.should_analyse_model = False

        self.should_validate_model = False
        self.should_validate_architecture = False

        self.should_export_for_resirio = False
        self.should_export_for_misim = False

        self.should_store_in_pickle_format = False
        self.resirio_export_should_be_js = False
        self.resirio_export_should_be_json = False
        self.should_be_lightweight_export = False
        self.should_be_pretty_print = False

        self.pattern = None

        self.latency = None
        self.custom_latency_format = None

        self.ask_for_resirio_or_misim_export()
        self.ask_for_pickle_export()
        if self.should_export_for_resirio:
            self.ask_for_additional_resirio_settings()
        print()
        self.ask_for_call_string_pattern()
        print()
        if self.should_export_for_misim:
            self.ask_for_latency()
            print()
        self.ask_for_analyses()
        print()
        self.ask_for_validations()

    def ask_for_analyses(self):
        analyse_model_answer = input("Do you want an analysis of the MODEL? <y> or <n>: ")
        self.should_analyse_model = True if analyse_model_answer == "y" else False

    def ask_for_validations(self):
        validate_model_answer = input("Do you want a validation of the MODEL? <y> or <n>: ")
        if self.should_export_for_resirio:
            validate_architecture_answer = input("Do you want a validation of the ARCHITECTURE? <y> or <n>: ")
            self.should_validate_architecture = True if validate_architecture_answer == "y" else False
        self.should_validate_model = True if validate_model_answer == "y" else False

    def ask_for_resirio_or_misim_export(self):
        export_type_answer = input("Do you want to create an architecture model for RESIRIO or MiSim? <r> or <m>: ")
        self.should_export_for_resirio = True if export_type_answer == "r" else False
        self.should_export_for_misim = True if export_type_answer == "m" else False

    def ask_for_pickle_export(self):
        should_store_in_pickle_format_answer = input(
            "Do you want to store the generic model in an intermediate format (pickle), too? <y> or <n>: ")
        self.should_store_in_pickle_format = True if should_store_in_pickle_format_answer == "y" else False

    def ask_for_additional_resirio_settings(self):
        resirio_export_data_type_answer = input("Do you want .js or .json as export type? <js> or <json>: ")
        should_be_lightweight_answer = input("Do you want the export of the graph to be lightweight? <y> or <n>: ")
        should_print_pretty_answer = input("Do you want a pretty print? <y> or <n>: ")
        self.resirio_export_should_be_json = True if resirio_export_data_type_answer == "json" else False
        self.resirio_export_should_be_js = True if resirio_export_data_type_answer == "js" else False
        self.should_be_lightweight_export = True if should_be_lightweight_answer == "y" else False
        self.should_be_pretty_print = True if should_print_pretty_answer == "y" else False

    def ask_for_call_string_pattern(self):
        print("Enter a Pattern for the spans that should be ignored. E.g.: GET-Requests.")
        print("Press Enter to use the default value (^GET$ for Jaeger and ^get$ for Zipkin)")
        self.pattern = input("Pattern as Python RegEx:")

    def ask_for_latency(self):
        self.latency = input("Insert a value for the default network latency (<ENTER> to skip this step):")
        self.custom_latency_format = input("Do want the format of the custom delay to be constant (mean) \n "
                                           "or mean with standard derivation? <m> or <mstd>: ")

    def __str__(self):
        output_string = "Analyse Model: " + str(self.should_analyse_model)
        output_string += "\nValidate Model: " + str(self.should_validate_model) + ", Validate Architecture: " + str(
            self.should_validate_architecture)
        output_string += "\nExport Model for " + ("RESIRIO" if self.should_export_for_resirio else "MiSim")
        output_string += ("\nAdditionally store in intermediate (pickle)-format: " + str(
            self.should_store_in_pickle_format)) if self.should_export_for_resirio else ""
        output_string += ("\nExport data-type: " + (
            ".json" if self.resirio_export_should_be_json else ".js")) if self.should_export_for_resirio else ""
        output_string += ("\nLightweight Export: " + str(
            self.should_be_lightweight_export)) if self.should_export_for_resirio else ""
        output_string += (
                    "\nPrint pretty: " + str(self.should_be_pretty_print)) if self.should_export_for_resirio else ""
        return output_string


def manual_input_test():
    settings_input = InteractiveSettingsInput()
    print("\nRegistered Settings:")
    print(settings_input)


if __name__ == "__main__":
    manual_input_test()
