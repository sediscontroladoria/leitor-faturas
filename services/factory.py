from services.leitor_sabesp import LeitorSabesp
from services.leitor_edp import LeitorEDP
from services.separador_faturas import SeparadorFaturas
from utils.regex_patterns import sabesp_patterns, edp_patterns

class ServiceFactory:    
    @staticmethod
    def get_leitor(tipo: str):
        if tipo == 'Sabesp':
            return LeitorSabesp()
        elif tipo == 'EDP':
            return LeitorEDP()
        return None

    @staticmethod
    def get_separador(tipo: str):
        if tipo == 'Sabesp':
            return SeparadorFaturas(sabesp_patterns['num_fatura'])
        elif tipo == 'EDP':
            return SeparadorFaturas(edp_patterns['num_fatura'])
        return None