from extractor.r_d_e.librede_host import LibReDE_Host
from extractor.r_d_e.librede_service import LibReDE_Service


# Creates a configuration file
class LibReDE_ConfigurationCreator:
    def __init__(self, hosts: list[LibReDE_Host], services: list[LibReDE_Service]):
        self.hosts = hosts
        self.services = services
        self.content: str = ""
        self.create_content()

    def create_content(self):
        self.content += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        self.content += "<librede:LibredeConfiguration xmi:version=\"2.0\" xmlns:xmi=\"http://www.omg.org/XMI\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:librede=\"http://www.descartes-research.net/librede/configuration/1.0\">\n"
        self.create_workload_description()
        self.create_input()
        self.create_estimation()
        self.create_output()
        self.create_validation()
        self.content += "</librede:LibredeConfiguration>"

    def get_csv_name(self) -> str:
        return "LibReDE_Configuration.librede"

    def create_workload_description(self):
        self.content += "<workloadDescription>\n"
        for host in self.hosts:
            host_demands = "demands=\""
            for service in host.services:
                host_demands += "//@workloadDescription/@services." + str(service.index) + "/@tasks." + str(host.index) + " "
            host_demands += "\""
            self.content += "   <resources name=\"" + host.name + "\" " + host_demands + "/>\n"
        for service in self.services:
            services_resource = "resource=\"//@workloadDescription/@resources." + str(service.host.index) + "\""
            self.content += "   <services name=\"" + service.operation_name + "\">\n"
            self.content += "       <tasks xsi:type=\"librede:ResourceDemand\" name=\"" + service.host.name + "\" " + services_resource + "/>\n"
            self.content += "   </services>\n"
        self.content += "</workloadDescription>\n"

    def create_input(self):
        self.content += "<input>\n"
        self.content += "   <dataSources name=\"Default\" type=\"tools.descartes.librede.datasource.csv.CsvDataSource\"/>\n"
        self.content += "</input>\n"

    def create_estimation(self):
        self.content += "<estimation>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.LiuOptimizationApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.ResponseTimeRegressionApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.WangKalmanFilterApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.ServiceDemandLawApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.KumarKalmanFilterApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.MenasceOptimizationApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.ResponseTimeApproximationApproach\"/>\n"
        self.content += "   <approaches type = \"tools.descartes.librede.approach.UtilizationRegressionApproach\"/>\n"
        self.content += "   <algorithms type = \"tools.descartes.librede.bayesplusplus.ExtendedKalmanFilter\"/>\n"
        self.content += "   <algorithms type = \"tools.descartes.librede.nnls.LeastSquaresRegression\"/>\n"
        self.content += "   <algorithms type = \"tools.descartes.librede.ipopt.java.RecursiveOptimization\"/>\n"
        self.content += "   <algorithms type = \"tools.descartes.librede.algorithm.SimpleApproximation\"/>\n"
        self.content += "   <stepSize value = \"60.0\">\n"
        self.content += "       <unit href = \"librede:units#SECONDS\"/>\n"
        self.content += "   </stepSize>\n"
        self.content += "   <startTimestamp>\n"
        self.content += "       <unit href = \"librede:units#SECONDS\"/>\n"
        self.content += "   </startTimestamp>\n"
        self.content += "   <endTimestamp>\n"
        self.content += "       <unit href = \"librede:units#SECONDS\"/>\n"
        self.content += "   </endTimestamp>\n"
        self.content += "</estimation>\n"

    def create_output(self):
        self.content += "<output>\n"
        self.content += "   <exporters name=\"Default Exporter\" type=\"tools.descartes.librede.export.csv.CsvExporter\">\n"
        self.content += "       <parameters name=\"OutputDirectory\" value=\"r-d-e_output\"/>\n"
        self.content += "       <parameters name=\"FileName\" value=\"abcd123\"/>\n"
        self.content += "   </exporters>\n"
        self.content += "</output>\n"

    def create_validation(self):
        self.content += "<validation>\n"
        self.content += "   <validators type = \"tools.descartes.librede.validation.AbsoluteUtilizationValidator\"/>\n"
        self.content += "   <validators type = \"tools.descartes.librede.validation.ResponseTimeValidator\"/>\n"
        self.content += "</validation>\n"
