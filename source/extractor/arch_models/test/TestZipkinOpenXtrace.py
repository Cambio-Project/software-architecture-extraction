import unittest
import os

from extractor.arch_models.test.TestUtil import TestUtil

class TestZipkinOpenXTrace(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Zipkin_OpenXTrace_MiSim(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'zipkin_trace_for_openxtrace.json')
        zipkin = TestUtil.loadZipkinMiSim(path_zipkin)["microservices"]

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_from_zipkin.json')
        openxtrace = TestUtil.loadOpenXTraceMiSim(path_openxtrace)["microservices"]
        TestUtil.MiSimBasicCheck(self, zipkin)
        TestUtil.MiSimBasicCheck(self, openxtrace)
        TestUtil.compareMiSim(self, openxtrace, zipkin)
    
    def test_Zipkin_OpenXTrace_MiSim_RoundRobin(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'zipkin_round_robin.json')
        zipkin = TestUtil.loadZipkinMiSim(path_zipkin)["microservices"]

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_round_robin.json')
        openxtrace = TestUtil.loadOpenXTraceMiSim(path_openxtrace)["microservices"]
        TestUtil.MiSimBasicCheck(self, zipkin)
        TestUtil.MiSimBasicCheck(self, openxtrace)
        TestUtil.compareMiSim(self, openxtrace, zipkin)

    def test_Zipkin_OpenXTrace_Resirio(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'zipkin_trace_for_openxtrace.json')
        zipkin = TestUtil.loadZipkinResirio(path_zipkin)

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'trace', 'open_xtrace_from_zipkin.json')
        openxtrace = TestUtil.loadOpenXTraceResirio(path_openxtrace)

        TestUtil.compareResirio(self, openxtrace, zipkin)

