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
from datetime import datetime

# Asks the user for all input in an interactive way via the command line.
# Prints all registered input to check whether everything is like the user wants.
user_input = InteractiveInput()
print()
print("Registered input:")
print(user_input)
print("----")
model_input = user_input.model_input
trace_input = user_input.trace_input
settings_input = user_input.settings_input


# Creates the respective IModel implementation (generic model) from the given input.
def create_generic_model():
    if model_input.contains_resirio_model:
        model_file_for_generic_model = model_input.get_model_file_path()
        return pickle.load(open(model_file_for_generic_model, 'rb'))
    elif model_input.contains_misim_model:
        model_file_for_generic_model = model_input.get_model_file_path()
        return MiSimModel(model_file_for_generic_model)
    elif trace_input.traces_are_jaeger:
        model_file_for_generic_model = ""  # TODO which model file?
        return JaegerTrace(model_file_for_generic_model, trace_input.contains_multiple_traces)
    elif trace_input.traces_are_zipkin:
        model_file_for_generic_model = ""  # TODO which model file?
        return ZipkinTrace(model_file_for_generic_model, trace_input.contains_multiple_traces)


# Creates the architecture for RESIRIO or MiSim out of the generic model.
def create_architecture():
    if generic_model is not None:
        if settings_input.should_export_for_resirio:
            return Architecture(generic_model)
        else:
            return ArchitectureMiSim(generic_model)


def validate():
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


def analyse():
    if settings_input.should_analyse_model and generic_model:
        generic_model.hazards = Analyzer.analyze_model(generic_model)


def export():
    current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    name_of_output_file = ("RESIRIO" if settings_input.should_export_for_resirio else "MiSim") + "-extraction_" + current_time
    if settings_input.should_store_in_pickle_format and generic_model is not None:
        pickle.dump(generic_model, open(name_of_output_file + "_pickle_export.dat", 'wb+'))  # stores the generic model in a binary format
    if settings_input.should_export_for_resirio:
        if generic_model is None:
            print("No model!")
            exit(1)
        if architecture is None:
            print("No architecture!")
            exit(1)
        export_file_type = "json" if settings_input.resirio_export_should_be_json or settings_input.should_export_for_misim else "js"
        export_type = export_file_type if settings_input.should_export_for_resirio else "MiSim"
        output_file = open(name_of_output_file + "." + export_file_type, 'w+')  # creates output file
        output_file.write(Exporter.export_architecture(architecture, export_type, settings_input.should_be_pretty_print, settings_input.should_be_lightweight_export))
        output_file.close()


# Main
generic_model = create_generic_model()
architecture = create_architecture()
validate()
analyse()
export()
