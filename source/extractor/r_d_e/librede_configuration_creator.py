from extractor.r_d_e.librede_host import LibredeHost
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


class LibredeConfigurationCreator:
    """
    Creates a LibReDE_Configuration-File out of the given hosts and services.
    """

    def __init__(self, hosts: list[LibredeHost], services: list[LibredeServiceOperation], path_for_input_files: str, path_for_output_files: str, start_timestamp: int, end_timestamp: int):
        self.hosts = hosts
        self.services = services
        self.path_for_input_files = path_for_input_files
        self.path_for_output_files = path_for_output_files
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.content = ""
        self.create_content()

    def get_path_to_configuration_file(self) -> str:
        return self.path_for_input_files + self.get_file_name()

    def get_file_name(self) -> str:
        return "LibReDE_Configuration_" + str(len(self.hosts)) + "hosts_" + str(len(self.services)) + "services.librede"

    def get_xml_content(self):
        return self.content

    def create_content(self):
        self.content += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        self.content += "<librede:LibredeConfiguration xmi:version=\"2.0\" xmlns:xmi=\"http://www.omg.org/XMI\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:librede=\"http://www.descartes-research.net/librede/configuration/1.0\">\n"
        self.create_workload_description()
        self.create_input()
        self.create_estimation()
        self.create_output()
        self.create_validation()
        self.content += "</librede:LibredeConfiguration>"

    def create_workload_description(self):
        self.content += "<workloadDescription>\n"
        for host in self.hosts:
            self.content += "   <resources name=\"host_" + host.name + "_id" + str(host.id) + "\"/>\n"
        for service in self.services:
            self.content += "   <services name=\"operation_" + service.operation_name + "_id" + str(service.id) + "\"/>\n"
        self.content += "</workloadDescription>\n"

    def create_input(self):
        self.content += "<input>\n"
        self.content += "   <dataSources name=\"CSV_Data\" type=\"tools.descartes.librede.datasource.csv.CsvDataSource\"/>\n"
        for service in self.services:
            self.content += "   <observations xsi:type=\"librede:FileTraceConfiguration\" metric=\"RESPONSE_TIME\" dataSource=\"//@input/@dataSources.0\" file=\"" + self.path_for_input_files + service.get_csv_file_name() + "\">\n"
            self.content += "       <mappings entity=\"//@workloadDescription/@services." + str(service.id) + "\"/>\n"
            self.content += "   </observations>\n"
        for host in self.hosts:
            self.content += "   <observations xsi:type=\"librede:FileTraceConfiguration\" metric=\"UTILIZATION\" dataSource=\"//@input/@dataSources.0\" file=\"" + self.path_for_input_files + host.get_csv_file_name() + "\">\n"
            self.content += "       <mappings entity=\"//@workloadDescription/@resources." + str(host.id) + "\"/>\n"
            self.content += "   </observations>\n"
        self.content += "</input>\n"

    def create_estimation(self):
        window: int = 60
        step_size: int = 120000
        self.content += "<estimation window=\"" + str(window) + "\" stepSize=\"" + str(step_size) + "\" startTimestamp=\"" + str(self.start_timestamp) + "\" endTimestamp=\"" + str(self.end_timestamp) + "\">\n"
        self.content += "   <approaches type=\"tools.descartes.librede.approach.ServiceDemandLawApproach\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.approach.ResponseTimeApproximationApproach\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.approach.WangKalmanFilterApproach\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.approach.ZhangKalmanFilterApproach\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.bayesplusplus.ExtendedKalmanFilter\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.nnls.LeastSquaresRegression\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.ipopt.java.RecursiveOptimization\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.algorithm.SimpleApproximation\"/>\n"
        self.content += "</estimation>\n"

    def create_output(self):
        output_file_name_prefix: str = ""
        self.content += "<output>\n"
        self.content += "   <exporters name=\"CSV_Export\" type=\"tools.descartes.librede.export.csv.CsvExporter\">\n"
        self.content += "       <parameters name=\"OutputDirectory\" value=\"" + self.path_for_output_files + "\"/>\n"
        self.content += "       <parameters name=\"FileName\" value=\"" + output_file_name_prefix + "\"/>\n"
        self.content += "   </exporters>\n"
        self.content += "</output>\n"

    def create_validation(self):
        self.content += "<validation/>\n"
