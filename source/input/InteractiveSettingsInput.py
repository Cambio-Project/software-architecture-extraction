from input.input_utils import get_valid_yes_no_input, get_valid_string_input_with_finite_valid_options, get_valid_string_input_with_predicates


class InteractiveSettingsInput:
    """
    Class which forces the user to type the input of the settings via the command line when instantiated.
    The input consists of three parts: Analyses, Validation and Export.
    """

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

        self.ask_for_settings()

    def ask_for_settings(self):
        export_type_answer = get_valid_string_input_with_finite_valid_options("Do you want to create an architecture model for RESIRIO or MiSim?", ["r", "m"])
        self.should_export_for_resirio = export_type_answer == "r"
        self.should_export_for_misim = export_type_answer == "m"
        self.should_store_in_pickle_format = get_valid_yes_no_input("Do you want to store the generic model in an intermediate format (pickle), too?")
        self.ask_for_additional_resirio_settings()
        self.ask_for_call_string_pattern()
        if self.should_export_for_misim:
            self.ask_for_latency()
        self.should_analyse_model = get_valid_yes_no_input("Do you want an analysis of the MODEL?")
        if self.should_export_for_resirio:
            self.should_validate_architecture = get_valid_yes_no_input("Do you want a validation of the ARCHITECTURE?")
        self.should_validate_model = get_valid_yes_no_input("Do you want a validation of the MODEL?")

    def ask_for_additional_resirio_settings(self):
        if self.should_export_for_resirio:
            resirio_export_data_type_answer = get_valid_string_input_with_finite_valid_options("Do you want .js or .json as export type?", ["js", "json"])
            self.resirio_export_should_be_js = resirio_export_data_type_answer == "js"
            self.resirio_export_should_be_json = resirio_export_data_type_answer == "json"
            self.should_be_lightweight_export = get_valid_yes_no_input("Do you want the export of the graph to be lightweight?")
            self.should_be_pretty_print = get_valid_yes_no_input("Do you want a pretty print?")

    def ask_for_call_string_pattern(self):
        self.pattern = get_valid_string_input_with_predicates("Enter a Pattern for the spans that should be ignored, e.g. GET-Requests.",
                                                              ["Pattern as Python RegEx", "Enter for default RegEx (^GET$ for Jaeger and ^get$ for Zipkin)"],
                                                              [lambda a: a != "", lambda a: a == ""])[1]

    def ask_for_latency(self):
        self.latency = get_valid_string_input_with_predicates("Insert a value for the default network latency.",
                                                              ["default_network_latency", "Enter to skip"],
                                                              [lambda a: a != "", lambda a: a == ""])[1]
        self.custom_latency_format = get_valid_string_input_with_finite_valid_options("Do want the format of the custom delay to be constant (mean) or"
                                                                                      " mean with standard derivation?",
                                                                                      ["m", "mstd"])

    def print_summary_of_settings_input(self):
        print("Analyse Model: " + str(self.should_analyse_model))
        print("Validate Model: " + str(self.should_validate_model))
        print("Validate Architecture: " + str(self.should_validate_architecture))
        print("Export Model for " + ("RESIRIO" if self.should_export_for_resirio else "MiSim"))
        print("Additionally store in intermediate (pickle)-format: " + str(self.should_store_in_pickle_format))
        if self.should_export_for_resirio:
            print("Export data-type: " + (".json" if self.resirio_export_should_be_json else ".js"))
            print("Lightweight Export: " + str(self.should_be_lightweight_export))
            print("Print pretty: " + str(self.should_be_pretty_print))
