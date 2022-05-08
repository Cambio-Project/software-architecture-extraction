# class which forces the input of a transformation model from the command line when instantiated
class TransformationModelInput:

    def __init__(self):
        self.isModel = False
        self.isMisim = False
        self.isJaeger = False
        self.isZipkin = False
        self.isMultiple = False

        self.file_location = None

        self.set_type()
        self.set_file_location()

    def set_type(self):
        model_type = input("possible types: <model>, <misim>, <jaeger>, <zipkin>, <multiple>\nType of model:")
        if model_type == "model":
            self.isModel = True
        elif model_type == "misim":
            self.isMisim = True
        elif model_type == "jaeger":
            self.isJaeger = True
        elif model_type == "zipkin":
            self.isZipkin = True
        elif model_type == "multiple":
            self.isMultiple = True
        else:
            pass  # error

    def set_file_location(self):
        self.file_location = input("File location:")

    def __str__(self):
        return "type: [" + str(self.isModel) + ", " + str(self.isMisim) + ", " + str(self.isJaeger) + ", " + str(
            self.isZipkin) + ", " + str(
            self.isMultiple) + "] out of " + "[model, misim, jaeger, zipkin, multiple]" + " at " + str(
            self.file_location)
