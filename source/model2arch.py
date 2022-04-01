import pickle
import argparse

from extractor.controllers.analyzer import Analyzer
from extractor.controllers.exporter import Exporter
from extractor.controllers.validator import Validator
from extractor.arch_models.architecture import Architecture
from extractor.arch_models.jaeger_trace import JaegerTrace
from extractor.arch_models.misim_model import MiSimModel
from extractor.arch_models.zipkin_trace import ZipkinTrace
from util.parse import bool_from_string


def cli():
    parser = argparse.ArgumentParser(description='Converts a model into an architecture representation.')

    # Transformation
    parser.add_argument('-m', '--model', dest='model', nargs=1, required=False, metavar='generic_model',
                        help='Stores a previously converted model.')
    parser.add_argument('--misim', dest='misim', type=str, nargs='+', required=False, metavar='misim_json_model',
                        help='Converts a MiSim model. Takes the architecture model and an optional experiment model.')
    parser.add_argument('--jaeger', dest='jaeger', type=str, nargs=1, required=False, metavar='jaeger_json_trace',
                        help='Converts a Jager trace.')
    parser.add_argument('--zipkin', dest='zipkin', type=str, nargs=1, required=False, metavar='zipkin_json_trace',
                        help='Converts a Zipkin trace.')
    parser.add_argument('--multiple', dest='multiple', action='store_true', required=False,
                        help='Can be used for Zipkin or Jaeger, when multiple traces are defined.')

    # Validation
    parser.add_argument('-vm', '--validate-model', dest='validate_model', action='store_true',
                        help='Validates the model.')
    parser.add_argument('-va', '--validate-architecture', dest='validate_architecture', action='store_true',
                        help='Validates the architecture.')

    # Analysis
    parser.add_argument('-am', '--analyze-model', dest='analyze_model', action='store_true',
                        help='Analyzes the model.')
    parser.add_argument('-aa', '--analyze-architecture', dest='analyze_architecture', action='store_true',
                        help='Analyzes the architecture.')

    # Export
    parser.add_argument('-em', '--export-model', dest='export_model', action='store_true',
                        help='Exports the converted model in an intermediate format (pickle).')
    parser.add_argument('-ea', '--export-architecture', dest='export_architecture', type=str, nargs='+', required=False,
                        metavar='export_type',
                        help='Stores a d3 graph and hazards of the architecture in the specified format '
                             '(either "js" or "json").')
    parser.add_argument('--lightweight', dest='lightweight', action='store_true', required=False,
                        help='Exports the graph without meta information.')

    args = parser.parse_args()
    model = None
    arch = None
    model_file = ''
    model_name = ''

    # Transformation
    if args.model:
        model_file = args.model[0]
        model = pickle.load(open(model_file, 'rb'))
    elif args.misim:
        model_file = args.misim[0]
        model = MiSimModel(model_file)
    elif args.jaeger:
        model_file = args.jaeger[0]
        model = JaegerTrace(model_file, args.multiple)
    elif args.zipkin:
        model_file = args.zipkin[0]
        model = ZipkinTrace(model_file, args.multiple)

    if model:
        model_name = model_file[model_file.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch = Architecture(model)

    # Validation
    if args.validate_model and model:
        success, exceptions = Validator.validate_model(model)
        success &= model.valid
        print('Validation of {} model: {} {}'.format(
            model.type,
            'Successful' if success else 'Failed',
            '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

    if args.validate_architecture and arch:
        success, exceptions = Validator.validate_architecture(arch)
        print('Validation of architecture: {} {}'.format(
            'Successful' if success else 'Failed',
            '' if not exceptions else '\n- ' + '\n- '.join(map(str, exceptions))))

    # Analysis
    if args.analyze_model and model:
        model.hazards = Analyzer.analyze_model(model)

    # Export
    if args.export_model:
        if model_file:
            pickle.dump(model, open(model_name + '_model_export.dat', 'wb+'))

    if args.export_architecture:

        stop = False

        if not model:
            print('No model!')
            stop = True
        if not arch:
            print('No architecture!')
            stop = True

        if stop:
            exit(1)

        export_type = 'js'
        pretty_print = False
        if args.export_architecture[0].lower() == 'json':
            export_type = 'json'
        if len(args.export_architecture) > 1 and bool_from_string(args.export_architecture[1]):
            pretty_print = True

        handle = open('{}_architecture_export.{}'.format(model_name, export_type), 'w+')
        handle.write(Exporter.export_architecture(arch, export_type, pretty_print, args.lightweight))
        handle.close()


if __name__ == '__main__':
    cli()
