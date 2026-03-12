from abc import ABC, abstractmethod

class Separador(ABC):
    @abstractmethod
    def separar(self, pdf_paths, pasta_saida):
        pass