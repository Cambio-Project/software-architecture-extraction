from source.input.InteractiveModelInput import InteractiveModelInput
from source.input.InteractiveTraceInput import InteractiveTraceInput
from source.input.InteractiveSettingsInput import InteractiveSettingsInput


# Class which forces the user to type all needed input via the command line when instantiated.
#
# First asks for a model which was previously created. If the user doesn't want to put in a model,
# the user gets asked to put in traces. Lastly, the user gets asked for settings.
class InteractiveInput:

    # Asks for either a RESIRIO- or MiSim-model or no model. Asks for traces if no model was given. Lastly, asks for settings.
    def __init__(self):
        self.model_input = InteractiveModelInput()
        print()
        if not self.model_input.contains_model():
            self.trace_input = InteractiveTraceInput()
            print()
        else:
            self.trace_input = None
        self.settings_input = InteractiveSettingsInput()

    def __str__(self):
        return "Model Input:\n" + str(self.model_input) + "\n\nTrace Input:\n" + str(self.trace_input) + "\n\nSettings:\n" + str(self.settings_input)


def main():
    all_input = InteractiveInput()
    print("\nRegistered Input:")
    print(all_input)


if __name__ == "__main__":
    main()
