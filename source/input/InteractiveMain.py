import pickle
from source.extractor.arch_models.jaeger_trace import JaegerTrace
from source.extractor.arch_models.misim_model import MiSimModel
from source.extractor.arch_models.zipkin_trace import ZipkinTrace
from source.input.AllInput import get_input

user_input = get_input()
extractor_input = user_input.extractor_input
resirio_settings = user_input.resirio_settings

model = None
arch = None
model_file = ''
model_name = ''
