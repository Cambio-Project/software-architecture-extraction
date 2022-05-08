# class which forces the input of a transformation model from the command line when instantiated
class AnalysesInput:
    def __init__(self):
        self.analyse_model = False
        self.analyse_architecture = False
        self.ask_for_analyses()

    def ask_for_analyses(self):
        analyse_model_answer = input("Do you want an analyses of the MODEL? <y> or <n>:")
        analyse_architecture_answer = input("Do you want an analyses of the ARCHITECTURE? <y> or <n>:")
        self.analyse_model = True if analyse_model_answer == "y" else False
        self.analyse_architecture = True if analyse_architecture_answer == "y" else False

    def __str__(self):
        return "analyse model: " + str(self.analyse_model) + ", analyse architecture: " + str(self.analyse_architecture)
