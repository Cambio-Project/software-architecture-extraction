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

generic_model = None
architecture = None
model_file_for_generic_model = ""
output_model_name = ""

if model_input.contains_resirio_model:
    model_file_for_generic_model = model_input.get_model_file_path()
    generic_model = pickle.load(open(model_file_for_generic_model, 'rb'))
elif model_input.contains_misim_model:
    model_file_for_generic_model = model_input.get_model_file_path()
    generic_model = MiSimModel(model_file_for_generic_model)
elif trace_input.traces_are_jaeger:
    model_file_for_generic_model = ""  # TODO which model file?
    generic_model = JaegerTrace(model_file_for_generic_model, trace_input.contains_multiple_traces)
elif trace_input.traces_are_zipkin:
    model_file_for_generic_model = ""  # TODO which model file?
    generic_model = ZipkinTrace(model_file_for_generic_model, trace_input.contains_multiple_traces)

if generic_model is not None:
    output_model_name = model_file_for_generic_model[model_file_for_generic_model.rfind('/') + 1:]
    output_model_name = output_model_name[:output_model_name.rfind('.')]
    if settings_input.should_export_for_misim:
        architecture = ArchitectureMiSim(generic_model)
    else:
        architecture = Architecture(generic_model)

# Validation
if settings_input.should_validate_model and generic_model is not None:
    success, exceptions = Validator.validate_model(generic_model)
    success &= generic_model.valid
    print('Validation of {} model: {} {}'.format(
        generic_model.type,
        'Successful' if success else 'Failed',
        '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

if settings_input.should_validate_architecture and architecture is not None:
    success, exceptions = Validator.validate_architecture(architecture)
    print('Validation of architecture: {} {}'.format(
        'Successful' if success else 'Failed',
        '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

# Analysis
if settings_input.should_analyse_model and generic_model:
    generic_model.hazards = Analyzer.analyze_model(generic_model)

# Export
if settings_input.should_store_in_pickle_format and model_file_for_generic_model is not None:
    pickle.dump(generic_model, open(output_model_name + "_model_export.dat", 'wb+'))
if settings_input.should_export_for_resirio:
    if generic_model is None:
        print("No model!")
        exit(1)
    if architecture is None:
        print("No architecture!")
        exit(1)
    export_type = "json" if settings_input.resirio_export_should_be_json or settings_input.should_export_for_misim else "js"
    model_type = export_type if settings_input.should_export_for_resirio else "MiSim"
    pretty_print = False
    if settings_input.should_be_pretty_print:
        pretty_print = True
    handle = open("{}_architecture_export.{}".format(output_model_name, export_type), 'w+')
    handle.write(Exporter.export_architecture(architecture, model_type, pretty_print, settings_input.should_be_lightweight_export))
    handle.close()
