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
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'zipkin_trace_for_openxtrace.json')
        zipkin = self.loadZipkinMiSim(path_zipkin)["microservices"]

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'open_xtrace_from_zipkin.json')
        openxtrace = self.loadOpenXTraceMiSim(path_openxtrace)["microservices"]
        self.checkMiSim(openxtrace)
        self.checkMiSim(openxtrace)
        self.compareMiSim(zipkin,openxtrace)
    
    def test_Zipkin_OpenXTrace_MiSim_RoundRobin(self):
        path_zipkin = os.path.join('source','extractor', 'arch_models', 'test', 'zipkin_round_robin.json')
        zipkin = self.loadZipkinMiSim(path_zipkin)["microservices"]

        path_openxtrace = os.path.join('source','extractor', 'arch_models', 'test', 'open_xtrace_round_robin.json')
        openxtrace = self.loadOpenXTraceMiSim(path_openxtrace)["microservices"]
        self.checkMiSim(zipkin)
        self.checkMiSim(openxtrace)
        self.compareMiSim(zipkin,openxtrace)
        
    def loadZipkinMiSim(self, path):
        model_zipkin = ZipkinTrace(path, False, "")
        if not model_zipkin:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_zipkin = ArchitectureMiSim(model_zipkin, "", "")
        return json.loads(arch_zipkin.export())

    def loadOpenXTraceMiSim(self, path):
        model_openxtrace = OpenXTrace(path, False, "")
        if not model_openxtrace:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_openxtrace = ArchitectureMiSim(model_openxtrace, "", "")
        return json.loads(arch_openxtrace.export())

    def checkMiSim(self, model: any): 
        for data in model:
            self.assertIsNotNone(data["name"])
            self.assertGreater(data["instances"], 0)
            self.assertIsNotNone(data["patterns"])
            self.assertIsNotNone(data["capacity"])
            self.assertIsNotNone(data["operations"])

    def compareMiSim(self, zipkin, openxtrace):
        for i in range(len(openxtrace)): 
            self.assertEqual(openxtrace[i]["name"].replace(" ", ""), zipkin[i]["name"].replace(" ", ""))
            self.assertEqual(openxtrace[i]["instances"], zipkin[i]["instances"])
            self.assertEqual(openxtrace[i]["capacity"], zipkin[i]["capacity"])
            if "loadbalancer_strategy" in openxtrace[i]:
                self.assertEqual(openxtrace[i]["loadbalancer_strategy"], zipkin[i]["loadbalancer_strategy"])
            self.assertEqual(openxtrace[i]["patterns"], zipkin[i]["patterns"])
            zipkin_operation = zipkin[i]["operations"]
            xtrace_operation = openxtrace[i]["operations"]
            self.assertEqual(len(zipkin_operation), len(xtrace_operation))
            for j in range(len(xtrace_operation)):
                self.assertEqual(xtrace_operation[j]["name"].replace(" ", ""), zipkin_operation[j]["name"].replace(" ", ""))
                self.assertEqual(xtrace_operation[j]["demand"], zipkin_operation[j]["demand"])
                zipkin_dependencies = zipkin_operation[j]["dependencies"]
                xtrace_dependencies= xtrace_operation[j]["dependencies"]
                self.assertEqual(len(zipkin_dependencies), len(xtrace_dependencies))
                for k in range(len(zipkin_dependencies)):
                    self.assertEqual(xtrace_dependencies[k]["service"].replace(" ", ""), zipkin_dependencies[k]["service"].replace(" ", ""))
                    self.assertEqual(xtrace_dependencies[k]["operation"].replace(" ", ""), zipkin_dependencies[k]["operation"].replace(" ", ""))
                    self.assertEqual(xtrace_dependencies[k]["probability"], zipkin_dependencies[k]["probability"])

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

