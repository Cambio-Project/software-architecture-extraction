import pickle
from source.extractor.arch_models.jaeger_trace import JaegerTrace
from source.extractor.arch_models.misim_model import MiSimModel
from source.extractor.arch_models.zipkin_trace import ZipkinTrace
from source.input.Input import getInput

user_input = getInput()
transformation_model_input = user_input.transformation_model_input
validations_input = user_input.validations_input
analyses_input = user_input.analyses_input
exports_input = user_input.exports_input

model = None
arch = None
model_file = ''
model_name = ''


def create_model_and_model_file():
    global model_file
    global model
    if transformation_model_input.isModel:
        model_file = transformation_model_input.file_location
        model = pickle.load(open(model_file, 'rb'))
    elif transformation_model_input.isMisim:
        model_file = transformation_model_input.file_location
        model = MiSimModel(model_file)
    elif transformation_model_input.isJaeger:
        model_file = transformation_model_input.file_location
        model = JaegerTrace(model_file, model_file)  # TODO add multiple instead of model file twice
    elif transformation_model_input.isZipkin:
        model_file = transformation_model_input.file_location
        model = ZipkinTrace(model_file, model_file)  # TODO add multiple instead of model file twice
        