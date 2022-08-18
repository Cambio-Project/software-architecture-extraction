import unittest
import os

from extractor.arch_models.test.TestUtil import TestUtil

class TestExporter(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Jaeger_MiSim(self):
        # Source of example setup used for jaeger_trace.json: https://github.com/orcas-elite/example-setups
        path = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'jaeger_trace.json')
        model = TestUtil.loadJaegerMiSim(path)["microservices"]
        TestUtil.MiSimBasicCheck(self, model)

    def test_OpenXtrace_MiSim(self):
        path = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_from_zipkin.json')
        model = TestUtil.loadOpenXTraceMiSim(path)["microservices"]
        TestUtil.MiSimBasicCheck(self, model)

    def test_Zipkin_MiSim(self): 
        # Source of example trace zipkin_trace.json: https://zipkin.io/pages/data_model.html
        path = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'jaeger_trace.json')
        model = TestUtil.loadZipkinMiSim(path)["microservices"]
        TestUtil.MiSimBasicCheck(self, model)