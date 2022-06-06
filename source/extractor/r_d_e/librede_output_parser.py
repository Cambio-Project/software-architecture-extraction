from extractor.r_d_e.librede_service import LibReDE_Service


class LibReDE_Output_Parser:
    def __init__(self, services: list[LibReDE_Service], path_to_output_files: str):
        self.test = 0
