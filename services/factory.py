from services.leitor_sabesp import LeitorSabesp
from services.separador_sabesp import SeparadorSabesp

class ServiceFactory:    
    @staticmethod
    def get_leitor(tipo: str):
        if tipo == "Sabesp":
            return LeitorSabesp()
        elif tipo == "EDP":
            pass
        return None

    @staticmethod
    def get_separador(tipo: str):
        if tipo == "Sabesp":
            return SeparadorSabesp()
        elif tipo == 'EDP':
            pass
        return None