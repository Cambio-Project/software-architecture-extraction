import unittest
import os

from extractor.arch_models.test.TestUti import TestUti

class TestZipkinOpenXTrace(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Zipkin_OpenXTrace_MiSim(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'zipkin_trace_for_openxtrace.json')
        zipkin = TestUti.loadZipkinMiSim(path_zipkin)["microservices"]

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_from_zipkin.json')
        openxtrace = TestUti.loadOpenXTraceMiSim(path_openxtrace)["microservices"]
        TestUti.MiSimBasicCheck(self, zipkin)
        TestUti.MiSimBasicCheck(self, openxtrace)
        TestUti.compareMiSim(self, openxtrace, zipkin)
    
    def test_Zipkin_OpenXTrace_MiSim_RoundRobin(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'zipkin_round_robin.json')
        zipkin = TestUti.loadZipkinMiSim(path_zipkin)["microservices"]

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_round_robin.json')
        openxtrace = TestUti.loadOpenXTraceMiSim(path_openxtrace)["microservices"]
        TestUti.MiSimBasicCheck(self, zipkin)
        TestUti.MiSimBasicCheck(self, openxtrace)
        TestUti.compareMiSim(self, openxtrace, zipkin)

    def test_Zipkin_OpenXTrace_Resirio(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'zipkin_trace_for_openxtrace.json')
        zipkin = TestUti.loadZipkinResirio(path_zipkin)

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_from_zipkin.json')
        openxtrace = TestUti.loadOpenXTraceResirio(path_openxtrace)

        TestUti.compareResirio(self, openxtrace, zipkin)

