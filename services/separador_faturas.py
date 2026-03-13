from abc import ABC, abstractmethod

class SeparadorFaturas(ABC):
    @abstractmethod
    def separar(self, pdf_paths, pasta_saida):
        pass