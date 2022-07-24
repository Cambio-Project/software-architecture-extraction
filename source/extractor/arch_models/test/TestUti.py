import json
from extractor.arch_models.architecture_misim import ArchitectureMiSim
from extractor.arch_models.open_xtrace import OpenXTrace
from extractor.arch_models.zipkin_trace import ZipkinTrace
from extractor.arch_models.architecture_resirio import ArchitectureResirio
from extractor.arch_models.jaeger_trace import JaegerTrace

class TestUti:

    @classmethod
    def loadJaegerMiSim(self, path):
        model = JaegerTrace(path, False, "")
        if not model:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_openxtrace = ArchitectureMiSim(model, "", "")
        return json.loads(arch_openxtrace.export())

    @classmethod
    def loadOpenXTraceMiSim(self, path):
        model = OpenXTrace(path, False, "")
        if not model:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_openxtrace = ArchitectureMiSim(model, "", "")
        return json.loads(arch_openxtrace.export())

    @classmethod
    def loadZipkinMiSim(self, path):
        model = ZipkinTrace(path, False, "")
        if not model:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_zipkin = ArchitectureMiSim(model, "", "")
        return json.loads(arch_zipkin.export())

    @classmethod
    def loadOpenXTraceResirio(self, path):
        model = OpenXTrace(path, False, "")
        if not model:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_openxtrace = ArchitectureResirio(model)
        return json.loads(arch_openxtrace.export())

    @classmethod
    def loadZipkinResirio(self, path):
        model = ZipkinTrace(path, False, "")
        if not model:
            return
        model_name = path[path.rfind('/') + 1:]
        model_name = model_name[:model_name.rfind('.')]
        arch_zipkin = ArchitectureResirio(model)
        return json.loads(arch_zipkin.export())

    @classmethod
    def MiSimBasicCheck(self, testclass, exportmodel):
        for data in exportmodel:
            testclass.assertIsNotNone(data["name"])
            testclass.assertGreater(data["instances"], 0)
            testclass.assertIsNotNone(data["patterns"])
            testclass.assertIsNotNone(data["capacity"])
            testclass.assertIsNotNone(data["operations"])

    @classmethod
    def compareMiSim(self, testclass, model1, model2):
        for i in range(len(model2)): 
            testclass.assertEqual(model2[i]["name"].replace(" ", ""), model1[i]["name"].replace(" ", ""))
            testclass.assertEqual(model2[i]["instances"], model1[i]["instances"])
            testclass.assertEqual(model2[i]["capacity"], model1[i]["capacity"])
            if "loadbalancer_strategy" in model2[i]:
                testclass.assertEqual(model2[i]["loadbalancer_strategy"], model1[i]["loadbalancer_strategy"])
            testclass.assertEqual(model2[i]["patterns"], model1[i]["patterns"])
            zipkin_operation = model1[i]["operations"]
            xtrace_operation = model2[i]["operations"]
            testclass.assertEqual(len(zipkin_operation), len(xtrace_operation))
            for j in range(len(xtrace_operation)):
                testclass.assertEqual(xtrace_operation[j]["name"].replace(" ", ""), zipkin_operation[j]["name"].replace(" ", ""))
                testclass.assertEqual(xtrace_operation[j]["demand"], zipkin_operation[j]["demand"])
                zipkin_dependencies = zipkin_operation[j]["dependencies"]
                xtrace_dependencies= xtrace_operation[j]["dependencies"]
                testclass.assertEqual(len(zipkin_dependencies), len(xtrace_dependencies))
                for k in range(len(zipkin_dependencies)):
                    testclass.assertEqual(xtrace_dependencies[k]["service"].replace(" ", ""), zipkin_dependencies[k]["service"].replace(" ", ""))
                    testclass.assertEqual(xtrace_dependencies[k]["operation"].replace(" ", ""), zipkin_dependencies[k]["operation"].replace(" ", ""))
                    testclass.assertEqual(xtrace_dependencies[k]["probability"], zipkin_dependencies[k]["probability"])
    
    @classmethod
    def compareResirio(self, testclass, model1, model2):
        model1_nodes = model1["nodes"]
        model1_edges = model1["edges"]
        model2_nodes = model2["nodes"]
        model2_edges = model2["edges"]
        testclass.assertEqual(len(model1_nodes), len(model2_nodes))
        testclass.assertEqual(len(model1_edges), len(model2_edges))
        
        for zipkin in model1_edges:
            zipkin = model1_edges[zipkin]
            label = zipkin["label"]
            source = model1_nodes[str(zipkin["source"])]
            target = model1_nodes[str(zipkin["target"])]
            index = -1
            for openxtrace in model2_edges:
                idx = openxtrace
                openxtrace = model2_edges[openxtrace]
                tmp = openxtrace["label"]
                tmp_source = model2_nodes[str(openxtrace["source"])]
                tmp_target = model2_nodes[str(openxtrace["target"])]
                if tmp == label and source["label"] == tmp_source["label"] and target["label"] == tmp_target["label"]:
                    index = idx
                    testclass.assertEqual(zipkin["data"]["tags"], openxtrace["data"]["tags"])
                    testclass.assertEqual(zipkin["data"]["logs"], openxtrace["data"]["logs"])
                    testclass.assertEqual(zipkin["data"]["duration"], openxtrace["data"]["duration"])
            
            testclass.assertNotEqual(index, -1)