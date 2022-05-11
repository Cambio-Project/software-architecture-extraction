from source.input.InteractiveExtractorInput import InteractiveExtractorInput
from source.input.InteractiveSettingsInput import InteractiveSettingsInput


# Class which forces the user to type all input via the command line when instantiated
class InteractiveInput:
    def __init__(self):
        self.extractor_input = InteractiveExtractorInput()
        self.settings_input = InteractiveSettingsInput()

    def __str__(self):
        return "Extractor Input:\n" + str(self.extractor_input) + "\n\nResirio Settings:\n" + str(
            self.settings_input) + "\n------"
