from input.InteractiveModelInput import InteractiveModelInput
from input.InteractiveTraceInput import InteractiveTraceInput
from input.InteractiveSettingsInput import InteractiveSettingsInput


class InteractiveInput:
    """
    Class which forces the user to type all needed input via the command line when instantiated.

    First asks for a model which was previously created (RESIRIO or  MiSim).
    If the user doesn't want to put in a model, the user gets asked to put in traces.
    Lastly, the user gets asked for settings.
    """

    def __init__(self):
        self.model_input = InteractiveModelInput()
        print()
        self.trace_input = None
        if not self.model_input.contains_model():
            self.trace_input = InteractiveTraceInput()
            print()
        self.settings_input = InteractiveSettingsInput()
        print("---------------------------------------------------------- Finished input of model, traces and settings.")

    def print_summary_of_input(self):
        self.model_input.print_summary_of_model_input()
        if self.trace_input is not None:
            self.trace_input.print_summary_of_trace_input()
        self.settings_input.print_summary_of_settings_input()
