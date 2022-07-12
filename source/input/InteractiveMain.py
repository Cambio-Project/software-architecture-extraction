import pickle
from typing import Optional

from extractor.arch_models.architecture_resirio import Architecture
from extractor.arch_models.architecture_misim import ArchitectureMiSim
from extractor.arch_models.jaeger_trace import JaegerTrace
from extractor.arch_models.misim_model import MiSimModel
from extractor.arch_models.zipkin_trace import ZipkinTrace
from extractor.controllers.analyzer import Analyzer
from extractor.controllers.exporter import Exporter
from extractor.controllers.validator import Validator
from extractor.r_d_e.librede_caller import LibredeCaller
from extractor.r_d_e.librede_input_creator import LibredeInputCreator
from input.InteractiveInput import InteractiveInput
from datetime import datetime


# Creates the respective IModel implementation (generic model) from the given input.
def create_generic_model(model_input, trace_input, settings_input):
    generic_model = None
    if model_input.contains_resirio_model:
        generic_model = pickle.load(open(model_input.get_model_file_path(), 'rb'))
    elif model_input.contains_misim_model:
        generic_model = MiSimModel(model_input.get_model_file_path())
    elif trace_input.traces_are_jaeger:
        generic_model = JaegerTrace(trace_input.get_traces(), trace_input.contains_multiple_traces, settings_input.pattern)
    elif trace_input.traces_are_zipkin:
        generic_model = ZipkinTrace(trace_input.get_traces(), trace_input.contains_multiple_traces, settings_input.pattern)
    call_librede_if_user_wants(generic_model)
    add_service_capacities(generic_model)
    return generic_model


# Creates the architecture for RESIRIO or MiSim out of the generic model.
def create_architecture(settings_input, generic_model):
    if settings_input.should_export_for_resirio:
        return Architecture(generic_model)
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


def call_librede_if_user_wants(generic_model) -> Optional[LibredeCaller]:
    """
    Asks the user whether LibReDE should be used to estimate the resource demands. As an alternative,
    the user can put in a default value as demand for every operation in the model.
    """
    print("----------------------------------------------------------\n")
    answer = input("Estimate Resource-Demands with LibReDE or with default demand? <y [for LibReDE]> or <int [positive integer as default demand for all operations]>: ")
    if answer == "y":
        return LibredeCaller(generic_model)
    elif answer != "":
        default_demand = int(answer)
        for service in generic_model.services.values():
            for operation in service.operations.values():
                operation.set_demand(default_demand)
    return None


def add_service_capacities(generic_model):
    """
    Asks the user whether the capacity of a service should be a custom default value for all services
    or should be read from a csv-File. Furthermore, fills in the capacities in the generic model.
    """
    answer = input("Set capacity of services: <int [positive integer as default capacity for all services]> or\n"
                   "    <path to csv [content must be like: \"service_name1,capacity1\\nservice_name2,capacity2,\\n etc.\"]>: ")
    if str.isdigit(answer):
        for service in generic_model.services.values():
            service.set_capacity(int(answer))
    else:
        capacity_file_handler = open(answer, "r")
        capacity_file_content = capacity_file_handler.read()
        lines: list[str] = capacity_file_content.split("\n")
        for line in lines:
            line_components = line.split(",")
            service_name = line_components[0]
            capacity_of_service = int(line_components[1])
            generic_model.services[service_name].set_capacity(capacity_of_service)
        capacity_file_handler.close()


def ask_user_whether_he_wants_a_summary_of_the_input(user_input: InteractiveInput, librede_input: LibredeInputCreator):
    """
    TODO
    """
    print()
    answer_of_user = input("Do you want a summary of all input (yours and of LibReDE)? <y> or <n>: ")
    if answer_of_user == "y":
        print()
        print("--------------------------------------------------------")
        print(str(user_input))
        print()
        print("LibReDE-input:")
        print(str(librede_input), end="")
        print("--------------------------------------------------------")


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


if __name__ == "__main__":
    main()
