import os.path
import pickle

from extractor.arch_models.architecture_resirio import ArchitectureResirio
from extractor.arch_models.architecture_misim import ArchitectureMiSim
from extractor.arch_models.jaeger_trace import JaegerTrace
from extractor.arch_models.misim_model import MiSimModel
from extractor.arch_models.open_xtrace import OpenXTrace
from extractor.arch_models.zipkin_trace import ZipkinTrace
from extractor.controllers.analyzer import Analyzer
from extractor.controllers.exporter import Exporter
from extractor.controllers.validator import Validator
from extractor.r_d_e.librede_caller import LibredeCaller
from input.InteractiveInput import InteractiveInput
from datetime import datetime

from input.input_utils import get_valid_string_input_with_predicates, str_is_int, get_valid_int_input, get_valid_yes_no_input


def create_generic_model(model_input, trace_input, settings_input):
    """
    Creates the respective IModel implementation (generic model) from the given input.
    """
    generic_model = None
    if model_input.contains_resirio_model:
        generic_model = pickle.load(open(model_input.get_model_file_path(), 'rb'))
    elif model_input.contains_misim_model:
        generic_model = MiSimModel(model_input.get_model_file_path())
    elif trace_input.traces_are_jaeger:
        generic_model = JaegerTrace(trace_input.get_traces(), False, settings_input.pattern)
    elif trace_input.traces_are_zipkin:
        generic_model = ZipkinTrace(trace_input.get_traces(), True, settings_input.pattern)
    elif trace_input.traces_are_open_x_trace:
        generic_model = OpenXTrace(trace_input.get_traces(), trace_input.get_number_of_traces() > 1, settings_input.pattern)
    add_service_capacities(generic_model)
    call_librede_if_user_wants(generic_model)
    return generic_model


def create_architecture(settings_input, generic_model):
    """
    Creates the architecture for RESIRIO or MiSim out of the generic model.
    """
    if settings_input.should_export_for_resirio:
        return ArchitectureResirio(generic_model)
    else:
        return ArchitectureMiSim(generic_model, settings_input.latency, settings_input.custom_latency_format)


def validate(settings_input, generic_model, architecture):
    if settings_input.should_validate_model:
        success, exceptions = Validator.validate_model(generic_model)
        success &= generic_model.valid
        print('Validation of {} model: {} {}'.format(
            generic_model.type,
            'Successful' if success else 'Failed',
            '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))
    if settings_input.should_validate_architecture:
        success, exceptions = Validator.validate_architecture(architecture)
        print('Validation of architecture: {} {}'.format(
            'Successful' if success else 'Failed',
            '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))


def analyse(settings_input, generic_model):
    if settings_input.should_analyse_model:
        generic_model.hazards = Analyzer.analyze_model(generic_model)


def export(settings_input, generic_model, architecture):
    current_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    name_of_output_file = (
                              "RESIRIO" if settings_input.should_export_for_resirio else "MiSim") + "-extraction_" + current_date
    if settings_input.should_store_in_pickle_format:
        pickle.dump(generic_model, open(name_of_output_file + "_pickle_export.dat",
                                        'wb+'))  # stores the generic model in a binary format
    export_file_type = "json" if settings_input.resirio_export_should_be_json or settings_input.should_export_for_misim else "js"
    export_type = export_file_type if settings_input.should_export_for_resirio else "MiSim"
    output_file = open(name_of_output_file + "." + export_file_type, 'w+')  # creates output file
    output_file.write(Exporter.export_architecture(architecture, export_type, settings_input.should_be_pretty_print,
                                                   settings_input.should_be_lightweight_export))
    output_file.close()


def call_librede_if_user_wants(generic_model):
    """
    Asks the user whether LibReDE should be used to estimate the resource demands. As an alternative,
    the user can put in a default value as demand for every operation in the model.
    """
    answer = get_valid_string_input_with_predicates("Estimate Resource-Demands with LibReDE or enter a default demand?",
                                                    ["y (for LibReDE)", "int (default demand for all operations)", "\"custom\" (set demand manually for each operation)"],
                                                    [lambda a: a == "y", lambda a: str_is_int(a), lambda a: a == "custom"])
    option_the_user_decided_for = answer[0]
    user_input = answer[1]
    if option_the_user_decided_for == 0:
        librede_caller = LibredeCaller(generic_model)
        librede_caller.print_summary()
    elif option_the_user_decided_for == 1:
        for service in generic_model.services.values():
            for operation in service.operations.values():
                operation.set_demand(int(user_input))
    else:
        for service in generic_model.services.values():
            for operation in service.operations.values():
                operation.set_demand(get_valid_int_input("Set demand for operation <" + operation.name + "> at service <" + service.name + ">."))


def add_service_capacities(generic_model):
    """
    Asks the user whether the capacity of a service should be a custom default value for all services
    or should be read from a csv-File. Furthermore, fills in the capacities in the generic model.
    """
    answer = get_valid_string_input_with_predicates("Set the capacity of the services.",
                                                    ["int (default for all services)", "\"manual\" (manual capacity for each service)", "Path to csv-file with capacities"],
                                                    [lambda a: str_is_int(a), lambda a: a == "manual", lambda a: os.path.isfile(a)])
    option_the_user_decided_for = answer[0]
    user_input = answer[1]
    if option_the_user_decided_for == 0:
        for service in generic_model.services.values():
            service.set_capacity(int(user_input))
    elif option_the_user_decided_for == 1:
        for service in generic_model.services.values():
            service.set_capacity(get_valid_int_input("Set capacity of service <" + service.name + ">: "))
    else:
        capacity_file_handler = open(user_input, "r")
        capacity_file_content = capacity_file_handler.read()
        lines: list[str] = capacity_file_content.split("\n")
        for line in lines:
            line_components = line.split(",")
            service_name = line_components[0].strip()
            capacity_of_service = int(line_components[1].strip())
            generic_model.services[service_name].set_capacity(capacity_of_service)
        capacity_file_handler.close()


def main():
    """
    Asks the user for all input in an interactive way via the command line.
    Creates the generic model and the architecture.
    Validation, Analyses, Export
    """
    user_input = InteractiveInput()
    model_input = user_input.model_input
    trace_input = user_input.trace_input
    settings_input = user_input.settings_input

    generic_model = create_generic_model(model_input, trace_input, settings_input)
    architecture = create_architecture(settings_input, generic_model)

    validate(settings_input, generic_model, architecture)
    analyse(settings_input, generic_model)
    export(settings_input, generic_model, architecture)

    user_input.print_summary_of_input()


if __name__ == "__main__":
    main()
