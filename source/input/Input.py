from source.input.AnalysesInput import AnalysesInput
from source.input.ExportsInput import ExportsInput
from source.input.TransformationModelInput import TransformationModelInput
from source.input.ValidationsInput import ValidationsInput


class Input:
    def __init__(self):
        self.transformation_model_input = TransformationModelInput()
        self.validations_input = ValidationsInput()
        self.analyses_input = AnalysesInput()
        self.exports_input = ExportsInput()

    def __str__(self):
        return "TransformModel: " + str(self.transformation_model_input) + "\n" + "Validations: " + str(
            self.validations_input) + "\n" + "Analyses: " + str(self.analyses_input) + "\n" + "Exports: " + str(
            self.exports_input)


def getInput():
    return Input()
