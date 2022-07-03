import json
import unittest
import os

from extractor.arch_models.zipkin_trace import ZipkinTrace
from extractor.arch_models.architecture_misim import ArchitectureMiSim
from extractor.arch_models.open_xtrace import OpenXTrace
from extractor.arch_models.architecture_resirio import Architecture


class TestZipkinOpenXTrace(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Zipkin_OpenXTrace_MiSim(self):
        model_file_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'zipkin_trace_for_openxtrace.json')
        model_zipkin = ZipkinTrace(model_file_zipkin, False, "")
        if not model_zipkin:
            return
        model_name = model_file_zipkin[model_file_zipkin.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_zipkin = ArchitectureMiSim(model_zipkin, "", "")
        exportmodel_zipkin = json.loads(arch_zipkin.export())

        model_file_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'open_xtrace_from_zipkin.json')
        model_openxtrace = OpenXTrace(model_file_openxtrace, False, "")
        if not model_openxtrace:
            return
        model_name = model_file_openxtrace[model_file_openxtrace.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_openxtrace = ArchitectureMiSim(model_openxtrace, "", "")
        exportmodel_openxtrace = json.loads(arch_openxtrace.export())



        for data in exportmodel_zipkin["microservices"]:
            self.assertIsNotNone(data["name"])
            self.assertGreater(data["instances"], 0)
            self.assertIsNotNone(data["patterns"])
            self.assertIsNotNone(data["capacity"])
            self.assertIsNotNone(data["operations"])
        for data in exportmodel_openxtrace["microservices"]:
            self.assertIsNotNone(data["name"])
            self.assertGreater(data["instances"], 0)
            self.assertIsNotNone(data["patterns"])
            self.assertIsNotNone(data["capacity"])
            self.assertIsNotNone(data["operations"])
        self.assertEqual(exportmodel_openxtrace, exportmodel_zipkin)

    def test_Zipkin_OpenXTrace_Resirio(self):
        model_file_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'zipkin_trace_for_openxtrace.json')
        model_zipkin = ZipkinTrace(model_file_zipkin, False, "")
        if not model_zipkin:
            return
        model_name = model_file_zipkin[model_file_zipkin.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_zipkin = Architecture(model_zipkin)
        exportmodel_zipkin = json.loads(arch_zipkin.export())

        model_file_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'open_xtrace_from_zipkin.json')
        model_openxtrace = OpenXTrace(model_file_openxtrace, False, "")
        if not model_openxtrace:
            return
        model_name = model_file_openxtrace[model_file_openxtrace.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_openxtrace = Architecture(model_openxtrace)
        exportmodel_openxtrace = json.loads(arch_openxtrace.export())


        zipkin_nodes = exportmodel_zipkin["nodes"]
        zipkin_edges = exportmodel_zipkin["edges"]
        openxtrace_nodes = exportmodel_openxtrace["nodes"]
        openxtrace_edges = exportmodel_openxtrace["edges"]
        self.assertEqual(len(zipkin_nodes), len(openxtrace_nodes))
        self.assertEqual(len(zipkin_edges), len(openxtrace_edges))
        
        for zipkin in zipkin_edges:
            zipkin = zipkin_edges[zipkin]
            label = zipkin["label"]
            source = zipkin_nodes[str(zipkin["source"])]
            target = zipkin_nodes[str(zipkin["target"])]
            index = -1
            for openxtrace in openxtrace_edges:
                idx = openxtrace
                openxtrace = openxtrace_edges[openxtrace]
                tmp = openxtrace["label"]
                tmp_source = openxtrace_nodes[str(openxtrace["source"])]
                tmp_target = openxtrace_nodes[str(openxtrace["target"])]
                if tmp == label and source["label"] == tmp_source["label"] and target["label"] == tmp_target["label"]:
                    index = idx
                    self.assertEqual(zipkin["data"]["tags"], openxtrace["data"]["tags"])
                    self.assertEqual(zipkin["data"]["logs"], openxtrace["data"]["logs"])
                    self.assertEqual(zipkin["data"]["duration"], openxtrace["data"]["duration"])
            
            self.assertNotEqual(index, -1)

