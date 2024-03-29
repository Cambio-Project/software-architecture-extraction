from extractor.arch_models.architecture_resirio import ArchitectureResirio


class Exporter:
    @staticmethod
    def export_architecture(arch: ArchitectureResirio, export_type: str, pretty: bool = False, lightweight: bool = False):
        # JavaScript
        if export_type == 'js':
            return 'const graph=' + arch.export(pretty) + ';'
        # Json
        elif export_type == 'json':
            return arch.export(pretty, lightweight)
        elif export_type == 'MiSim':
            return arch.export()
