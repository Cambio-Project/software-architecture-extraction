from source.input.ExtractorInput import ExtractorInput
from source.input.ResirioSettingsInput import ResirioSettingsInput


# class which forces the user to type all input via the command line when instantiated
class AllInput:
    def __init__(self):
        self.extractor_input = ExtractorInput()
        print()
        self.resirio_settings = ResirioSettingsInput()

    def __str__(self):
        return "Extractor Input:\n" + str(self.extractor_input) + "\n\nResirio Settings:\n" + str(
            self.resirio_settings) + "\n------"


def get_input():
    return AllInput()


all_input = get_input()
print("\nRegistered input:\n" + str(all_input))
