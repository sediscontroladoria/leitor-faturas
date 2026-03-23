from services.leitor_sabesp import LeitorSabesp
from services.leitor_edp import LeitorEDP
from services.separador_faturas import SeparadorFaturas

from utils.regex_patterns import sabesp_patterns
from utils.headers import sabesp_headers, edp_headers

from utils.mapeamentos import (
    RGI_FICHA_SABESP, RGI_FICHA_SABESP_CENTRO, RGI_SABESP, RGI_SABESP_CENTRO,
    UC_FICHA_EDP, UC_FICHA_EDP_CENTRO, UC_EDP, UC_EDP_CENTRO
)

class ServiceFactory:    
    @staticmethod
    def get_configuracao_fatura(tipo_fatura: str, is_centro_comunitario: bool) -> dict:

        if tipo_fatura == 'Sabesp':
            return {
                'leitor': LeitorSabesp(),
                'separador': SeparadorFaturas(sabesp_patterns['num_fatura']),
                'mapa_fichas': RGI_FICHA_SABESP_CENTRO if is_centro_comunitario else RGI_FICHA_SABESP,
                'lista_ordenacao': RGI_SABESP_CENTRO if is_centro_comunitario else RGI_SABESP,
                'headers': sabesp_headers,
                'coluna_id': 'rgi'
            }
        
        elif tipo_fatura == 'EDP':
            return {
                'leitor': LeitorEDP(),
                'separador': SeparadorFaturas(),
                'mapa_fichas': UC_FICHA_EDP_CENTRO if is_centro_comunitario else UC_FICHA_EDP,
                'lista_ordenacao': UC_EDP_CENTRO if is_centro_comunitario else UC_EDP,
                'headers': edp_headers,
                'coluna_id': 'uc'
            }
        
        raise ValueError(f"Tipo de fatura '{tipo_fatura}' não suportado.")