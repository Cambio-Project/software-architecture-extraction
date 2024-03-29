from typing import List

from extractor.arch_models.hazard import Hazard
from extractor.arch_models.model import IModel


class Analyzer:
    @staticmethod
    def analyze_model(model: IModel) -> List[Hazard]:
        return model.analyze()
