import pickle

from source.extractor.arch_models.architecture import Architecture
from source.extractor.arch_models.architecture_misim import ArchitectureMiSim
from source.extractor.arch_models.jaeger_trace import JaegerTrace
from source.extractor.arch_models.misim_model import MiSimModel
from source.extractor.arch_models.zipkin_trace import ZipkinTrace
from source.extractor.controllers.analyzer import Analyzer
from source.extractor.controllers.exporter import Exporter
from source.extractor.controllers.validator import Validator
from source.input.InteractiveInput import InteractiveInput

user_input = InteractiveInput()
print()
print("Registered input:")
print(user_input)
print("----")
model_input = user_input.model_input
trace_input = user_input.trace_input
settings_input = user_input.settings_input

model = None
arch = None
model_file = ''
model_name = ''

if model_input.contains_resirio_model:
    model_file = model_input.get_model_file_path()
    model = pickle.load(open(model_file, 'rb'))
elif model_input.contains_misim_model:
    model_file = model_input.get_model_file_path()
    model = MiSimModel(model_file)
elif trace_input.traces_are_jaeger:
    model_file = ""  # TODO which model file?
    model = JaegerTrace(model_file, trace_input.contains_multiple_traces)
elif trace_input.traces_are_zipkin:
    model_file = ""  # TODO which model file?
    model = ZipkinTrace(model_file, trace_input.contains_multiple_traces)

if model is not None:
    model_name = model_file[model_file.rfind('/') + 1:]
    model_name = model_name[:model_name.rfind('.')]
    if settings_input.should_export_for_misim:
        arch = ArchitectureMiSim(model)
    else:
        arch = Architecture(model)

# Validation
if settings_input.should_validate_model and model is not None:
    success, exceptions = Validator.validate_model(model)
    success &= model.valid
    print('Validation of {} model: {} {}'.format(
        model.type,
        'Successful' if success else 'Failed',
        '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

if settings_input.should_validate_architecture and arch is not None:
    success, exceptions = Validator.validate_architecture(arch)
    print('Validation of architecture: {} {}'.format(
        'Successful' if success else 'Failed',
        '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

# Analysis
if settings_input.should_analyse_model and model:
    model.hazards = Analyzer.analyze_model(model)

# Export
if settings_input.should_store_in_pickle_format:
    if model_file:
        pickle.dump(model, open(model_name + '_model_export.dat', 'wb+'))
if settings_input.should_export_for_resirio:
    if model is None:
        print('No model!')
        exit(1)
    if arch is None:
        print('No architecture!')
        exit(1)
    export_type = 'json' if settings_input.resirio_export_should_be_json or settings_input.should_export_for_misim else 'js'
    model_type = export_type if settings_input.should_export_for_resirio else "MiSim"
    pretty_print = False
    if settings_input.should_be_pretty_print:
        pretty_print = True
    handle = open('{}_architecture_export.{}'.format(model_name, export_type), 'w+')
    handle.write(Exporter.export_architecture(arch, model_type, pretty_print, settings_input.should_be_lightweight_export))
    handle.close()
