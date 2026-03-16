from dataclasses import dataclass
from models.fatura_base import Fatura

@dataclass
class FaturaEDP(Fatura):
    uc: str
    medidor: str

    @property
    def identificador_ligacao(self) -> str:
        return self.uc

    def __str__(self):
        return '\n'.join([f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in vars(self).items()])