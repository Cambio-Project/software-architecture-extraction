from extractor.r_d_e.librede_host import LibredeHost
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


# Creates a LibReDE_Configuration-File out of the given hosts and services.
class LibReDE_ConfigurationCreator:

    def __init__(self, hosts: list[LibredeHost], services: list[LibredeServiceOperation], path_for_input_files: str, path_for_output_files: str):
        self.hosts = hosts
        self.services = services
        self.path_for_input_files = path_for_input_files
        self.path_for_output_files = path_for_output_files
        self.content = ""
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

    def get_path_to_configuration_file(self) -> str:
        return self.path_for_input_files + self.get_file_name()

    def get_file_name(self) -> str:
        return "LibReDE_Configuration_" + str(len(self.hosts)) + "hosts_" + str(len(self.services)) + "services.librede"

    def create_workload_description(self):
        self.content += "<workloadDescription>\n"
        for host in self.hosts:
            self.content += "   <resources name=\"" + host.name + "\"/>\n"
        for service in self.services:
            self.content += "   <services name=\"" + service.operation_name + "_" + service.host.name + "\"/>\n"
        self.content += "</workloadDescription>\n"

    def create_input(self):
        interval: int = 30000
        self.content += "<input>\n"
        self.content += "   <dataSources name=\"Default_Data_Source_Type\" type=\"tools.descartes.librede.datasource.csv.CsvDataSource\"/>\n"
        for service in self.services:
            self.content += "   <observations xsi:type=\"librede:FileTraceConfiguration\" metric=\"RESPONSE_TIME\" dataSource=\"//@input/@dataSources.0\" file=\"" + self.path_for_input_files + service.get_csv_file_name() + "\">\n"
            self.content += "       <mappings entity=\"//@workloadDescription/@services." + str(service.id) + "\"/>\n"
            self.content += "   </observations>\n"
        for host in self.hosts:
            self.content += "   <observations xsi:type=\"librede:FileTraceConfiguration\" metric=\"UTILIZATION\" interval=\"" + str(interval) + "\" dataSource=\"//@input/@dataSources.0\" file=\"" + self.path_for_input_files + host.get_csv_file_name() + "\">\n"
            self.content += "       <mappings entity=\"//@workloadDescription/@resources." + str(host.id) + "\"/>\n"
            self.content += "   </observations>\n"
        self.content += "</input>\n"

    def create_estimation(self):
        window: int = 60
        step_size: int = 120000
        start_timestamp: int = 1370087550000
        end_timestamp: int = 1370090939000
        self.content += "<estimation window=\"" + str(window) + "\" stepSize=\"" + str(step_size) + "\" startTimestamp=\"" + str(start_timestamp) + "\" endTimestamp=\"" + str(end_timestamp) + "\">\n"
        self.content += "   <approaches type=\"tools.descartes.librede.approach.ResponseTimeRegressionApproach\"/>\n"
        self.content += "   <approaches type=\"tools.descartes.librede.approach.ServiceDemandLawApproach\"/>\n"
        self.content += "</estimation>\n"

    def create_output(self):
        output_file_name_prefix: str = "generation"
        self.content += "<output>\n"
        self.content += "   <exporters name=\"Default_CSV_Exporter\" type=\"tools.descartes.librede.export.csv.CsvExporter\">\n"
        self.content += "       <parameters name=\"OutputDirectory\" value=\"" + self.path_for_output_files + "\"/>\n"
        self.content += "       <parameters name=\"FileName\" value=\"" + output_file_name_prefix + "\"/>\n"
        self.content += "   </exporters>\n"
        self.content += "</output>\n"

    def create_validation(self):
        validation_folds: int = 5
        validation_estimates: bool = True
        self.content += "<validation validationFolds=\"" + str(validation_folds) + "\" validateEstimates=\"" + str(validation_estimates).lower() + "\">\n"
        self.content += "   <validators type=\"tools.descartes.librede.validation.ResponseTimeValidator\"/>\n"
        self.content += "   <validators type=\"tools.descartes.librede.validation.UtilizationValidator\"/>\n"
        self.content += "</validation>\n"