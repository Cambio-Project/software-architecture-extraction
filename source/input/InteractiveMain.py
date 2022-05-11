import pickle
from source.extractor.arch_models.jaeger_trace import JaegerTrace
from source.extractor.arch_models.misim_model import MiSimModel
from source.extractor.arch_models.zipkin_trace import ZipkinTrace
from source.input.InteractiveInput import InteractiveInput

user_input = InteractiveInput()
extractor_input = user_input.extractor_input
settings_input = user_input.settings_input

model = None
arch = None
model_file = ''
model_name = ''
