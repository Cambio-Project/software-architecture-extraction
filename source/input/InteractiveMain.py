import pickle
from source.extractor.arch_models.jaeger_trace import JaegerTrace
from source.extractor.arch_models.misim_model import MiSimModel
from source.extractor.arch_models.zipkin_trace import ZipkinTrace
from source.input.AllInput import get_input

user_input = get_input()
transformation_model_input = user_input.transformation_model_input
validations_input = user_input.validations_input
analyses_input = user_input.analyses_input
exports_input = user_input.exports_input

model = None
arch = None
model_file = ''
model_name = ''

        