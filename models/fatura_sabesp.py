from dataclasses import dataclass

@dataclass
class FaturaSabesp:
    num_documento: str
    rgi: str
    hidrometro: str
    valor: str
    consumo: str
    vencimento: str
    debito_automatico: str
    retencao_ir: str

    def __str__(self):
        return '\n'.join([f'{k.replace('_', ' ').capitalize()}: {v}' for k, v in vars(self).items()])

