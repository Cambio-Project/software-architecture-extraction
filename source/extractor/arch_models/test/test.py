import json
import unittest

from ...arch_models.jaeger_trace import JaegerTrace
from ...arch_models.zipkin_trace import ZipkinTrace
from ...arch_models.architecture_misim import ArchitectureMiSim


class TestExporter(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_Zipkin_MiSim(self):
        # Source of example trace zipkin_trace.json: https://zipkin.io/pages/data_model.html
        model_file = str('./extractor/arch_models/test/zipkin_trace.json')
        model = ZipkinTrace(model_file, False)
        if not model:
            return
        model_name = model_file[model_file.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch = ArchitectureMiSim(model)
        exportmodel = json.loads(arch.export())
        for data in exportmodel["microservices"]:
            self.assertIsNotNone(data["name"])
            self.assertGreater(data["instances"], 0)
            self.assertIsNotNone(data["patterns"])
            self.assertIsNotNone(data["capacity"])
            self.assertIsNotNone(data["operations"])

    def test_Jaeger_MiSim(self):
        # Source of example setup used for jaeger_trace.json: https://github.com/orcas-elite/example-setups
        model_file = str('./extractor/arch_models/test/jaeger_trace.json')
        model = JaegerTrace(model_file, False)
        if not model:
            return
        model_name = model_file[model_file.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch = ArchitectureMiSim(model)
        exportmodel = json.loads(arch.export())
        for data in exportmodel["microservices"]:
            self.assertIsNotNone(data["name"])
            self.assertGreater(data["instances"], 0)
            self.assertIsNotNone(data["patterns"])
            self.assertIsNotNone(data["capacity"])
            self.assertIsNotNone(data["operations"])