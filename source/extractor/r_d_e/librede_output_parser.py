from extractor.r_d_e.librede_service import LibReDE_Service


class LibReDE_Output_Parser:
    def __init__(self, services: list[LibReDE_Service], path_to_output_files: str):
        self.services = services
        self.path_to_output_files = path_to_output_files

    def get_results_of_librede(self) -> dict[str, int]:
        pass
