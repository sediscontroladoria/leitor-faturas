import pandas as pd
from utils.constants import RGI_SABESP
from dataclasses import asdict

class ProcessadorDados:
    @staticmethod
    def preparar_dataframe_faturas(faturas_lidas: list, mapa_rgi_ficha: dict, headers: dict) -> pd.DataFrame:
        """
        Abstrai a transformação de faturas em um DataFrame formatado e pronto para exportação.
        """
        faturas_dicts = [asdict(f) for f in faturas_lidas]
        
        df = pd.DataFrame(faturas_dicts)
        
        df['ficha'] = df['rgi'].map(mapa_rgi_ficha).fillna('Sem Ficha')
        
        df = ProcessadorDados.ordenar_por_rgi(df)
        
        return df.rename(columns=headers)
    
    @staticmethod
    def ordenar_por_rgi(df: pd.DataFrame, coluna_rgi: str = 'rgi') -> pd.DataFrame:
        df[coluna_rgi] = pd.Categorical(
            df[coluna_rgi], 
            categories=RGI_SABESP, 
            ordered=True
        )
        return df.sort_values(coluna_rgi)