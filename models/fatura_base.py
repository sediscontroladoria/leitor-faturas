from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Fatura(ABC):
    num_fatura: str
    valor: str
    consumo: str
    vencimento: str
    debito_automatico: str
    retencao_ir: str

    @property
    @abstractmethod
    def identificador_ligacao(self) -> str:
        pass