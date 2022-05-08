# class which forces the input of the exports from the command line when instantiated
class ExportsInput:
    def __init__(self):
        self.should_export_model = False
        self.should_export_architecture = False
        self.should_be_lightweight = False
        self.ask_for_exports()

    def ask_for_exports(self):
        should_export_model_answer = input("Do you want to export the MODEL? <y> or <n>:")
        should_export_architecture_answer = input("Do you want to export the ARCHITECTURE? <y> or <n>:")
        should_be_lightweight_answer = input("Do you want the export of the graph lightweight? <y> or <n>:")
        self.should_export_model = True if should_export_model_answer == "y" else False
        self.should_export_architecture = True if should_export_architecture_answer == "y" else False
        self.should_be_lightweight = True if should_be_lightweight_answer == "y" else False

    def __str__(self):
        return "export model: " + str(self.should_export_model) + ", export architecture: " + str(
            self.should_export_architecture) + ", export is lightweight: " + str(self.should_be_lightweight)
