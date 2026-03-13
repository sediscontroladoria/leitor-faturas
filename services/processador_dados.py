import pandas as pd
from utils.constants import RGI_ORDEM_SABESP

class ProcessadorDados:
    @staticmethod
    def ordenar_por_rgi(df: pd.DataFrame, coluna_rgi: str = 'rgi') -> pd.DataFrame:
        df[coluna_rgi] = pd.Categorical(
            df[coluna_rgi], 
            categories=RGI_ORDEM_SABESP, 
            ordered=True
        )
        return df.sort_values(coluna_rgi)