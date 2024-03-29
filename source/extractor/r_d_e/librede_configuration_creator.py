from extractor.r_d_e.librede_host import LibredeHost
from extractor.r_d_e.librede_service_operation import LibredeServiceOperation


class LibredeConfigurationCreator:
    """
    Creates a LibReDE_Configuration-File out of the given service.
    """

    def __init__(self, service_operation: LibredeServiceOperation, approaches: list[str], path_for_input_files: str, path_for_output_files: str):
        self.service_operation = service_operation
        self.host: LibredeHost = service_operation.host
        self.path_for_input_files = path_for_input_files
        self.path_for_output_files = path_for_output_files
        self.start_timestamp = int(self.host.start_time / 10 ** 3)
        self.end_timestamp = int(self.host.end_time / 10 ** 3)
        self.approaches = approaches
        self.content = ""
        self.create_content()

    def get_path_to_configuration_file(self) -> str:
        return self.path_for_input_files + self.get_file_name()

    def get_file_name(self) -> str:
        return "configuration_" + str(self.host.id) + "_" + str(self.service_operation.id) + ".librede"

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
        self.content += "   <resources name=\"host" + str(self.host.id) + "\"/>\n"
        self.content += "   <services name=\"op" + str(self.service_operation.id) + "\"/>\n"
        self.content += "</workloadDescription>\n"

    def create_input(self):
        self.content += "<input>\n"
        self.content += "   <dataSources name=\"CSV_Data\" type=\"tools.descartes.librede.datasource.csv.CsvDataSource\"/>\n"
        self.content += "   <observations xsi:type=\"librede:FileTraceConfiguration\" metric=\"RESPONSE_TIME\" dataSource=\"//@input/@dataSources.0\" file=\"" + self.path_for_input_files + self.service_operation.get_csv_file_name() + "\">\n"
        self.content += "       <mappings entity=\"//@workloadDescription/@services.0\"/>\n"
        self.content += "   </observations>\n"
        self.content += "   <observations xsi:type=\"librede:FileTraceConfiguration\" metric=\"UTILIZATION\" dataSource=\"//@input/@dataSources.0\" file=\"" + self.path_for_input_files + self.host.get_csv_file_name() + "\">\n"
        self.content += "       <mappings entity=\"//@workloadDescription/@resources.0\"/>\n"
        self.content += "   </observations>\n"
        self.content += "</input>\n"

    def create_estimation(self):
        window = len(self.service_operation.response_times)
        step_size = int((self.end_timestamp - self.start_timestamp) / window)
        self.content += "<estimation window=\"" + str(window) + "\" stepSize=\"" + str(step_size) + "\" startTimestamp=\"" + str(self.start_timestamp) + "\" endTimestamp=\"" + str(self.end_timestamp) + "\">\n"
        for approach in self.approaches:
            self.content += "   <approaches type=\"tools.descartes.librede.approach." + approach + "\"/>\n"
        self.content += "</estimation>\n"

    def create_output(self):
        output_file_name_prefix: str = str(self.service_operation.id)
        self.content += "<output>\n"
        self.content += "   <exporters name=\"CSV_Export\" type=\"tools.descartes.librede.export.csv.CsvExporter\">\n"
        self.content += "       <parameters name=\"OutputDirectory\" value=\"" + self.path_for_output_files + "\"/>\n"
        self.content += "       <parameters name=\"FileName\" value=\"" + output_file_name_prefix + "\"/>\n"
        self.content += "   </exporters>\n"
        self.content += "</output>\n"

    def create_validation(self):
        self.content += "<validation/>\n"


def create_configurations(service_operations: list[LibredeServiceOperation], approaches: list[str],
                          path_for_input_files: str, path_for_output_files: str) -> list[LibredeConfigurationCreator]:
    """
    Creates a configuration for every given service.
    """
    configurations = list[LibredeConfigurationCreator]()
    for service_operation in service_operations:
        configurations.append(LibredeConfigurationCreator(service_operation, approaches, path_for_input_files, path_for_output_files))
    return configurations
