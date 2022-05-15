from typing import Tuple, List

from extractor.arch_models.architecture_resirio import Architecture
from extractor.arch_models.model import IModel


class Validator:
    @staticmethod
    def validate_model(model: IModel) -> Tuple[bool, List[BaseException]]:
        return model.validate(True)

    @staticmethod
    def validate_architecture(arch: Architecture) -> Tuple[bool, List[BaseException]]:
        return arch.validate()
