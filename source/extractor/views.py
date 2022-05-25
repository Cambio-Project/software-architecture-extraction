import json
import zipfile

from django.http import HttpResponse
from .arch_models.architecture_resirio import Architecture
from .arch_models.jaeger_trace import JaegerTrace
from .arch_models.misim_model import MiSimModel
from .arch_models.zipkin_trace import ZipkinTrace
from .controllers.analyzer import Analyzer
from .controllers.exporter import Exporter
from .models.architecture import ArchitectureModel
from ..util.log import error


def upload(request):
    try:
        model = None
        file = request.FILES['file']
        content = json.load(file)
        lightweight = False

        if ArchitectureModel.objects.filter(name=file).exists():
            return HttpResponse('Model does exist already. Please choose another name.', status=500)

        # Load model
        try:
            if isinstance(content, dict):
                if content.get('microservices', False):
                    model = MiSimModel(content)
                elif content.get('data', False):
                    model = JaegerTrace(content)
            elif isinstance(content, list):
                multiple = True if isinstance(content[0], list) else False
                lightweight = multiple
                model = ZipkinTrace(content, multiple)

        except BaseException as e:
            error(e)
            return HttpResponse('Processing error: Model could not be read.', status=500)

        if model:

            # Validate
            success, exceptions = model.validate(True)
            if not success:
                return HttpResponse('Validation error: ' + '\n- ' + '\n- '.join(map(str, exceptions)), status=500)

            # Analyze
            model.analyze()

        # Create architecture
        if model:
            arch = Architecture(model)
            export = Exporter.export_architecture(arch, 'JSON', lightweight)

            # Store architecture in DB
            try:
                ArchitectureModel.objects.create(name=file, content=export)

            except BaseException as e:
                error(e)
                return HttpResponse('File to big', status=500)

        else:
            return HttpResponse('Wrong format', status=500)

        return HttpResponse(status=200)

    except BaseException as e:
        error(e)
        return HttpResponse('Processing error: Unknown error.', status=500)


def export_arch(request):
    try:
        response = HttpResponse(content_type='application/zip')
        archive = zipfile.ZipFile(response, 'w')

        for obj in ArchitectureModel.objects.all():
            archive.writestr(obj.name, obj.content)

        response['Content-Disposition'] = 'attachment; filename={}'.format('export.zip')
        return response

    except BaseException as e:
        error(e)
        return HttpResponse('Processing error', status=500)


def import_arch(request):
    return HttpResponse('', status=200)
