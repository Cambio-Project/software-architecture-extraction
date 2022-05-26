from typing import List

from source.extractor.arch_models.hazard import Hazard
from source.extractor.arch_models.model import IModel


class Analyzer:
    @staticmethod
    def analyze_model(model: IModel) -> List[Hazard]:
        return model.analyze()
