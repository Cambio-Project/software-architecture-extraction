from source.input.ExtractorInput import ExtractorInput
from source.input.ResirioSettingsInput import ResirioSettingsInput


class Input:
    def __init__(self):
        self.extractor_input = ExtractorInput()
        print()
        self.resirio_settings = ResirioSettingsInput()

    def __str__(self):
        return str(self.extractor_input) + "\n" + str(self.resirio_settings)


def get_input():
    return Input()


extractor_input = get_input()
print("\nRegistered input:\n" + str(extractor_input))
