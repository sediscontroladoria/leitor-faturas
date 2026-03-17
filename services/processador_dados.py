import pandas as pd
import re
from utils.constants import RGI_SABESP, UC_EDP, DOTACAO_FIXA, RELACAO_FICHAS_ORCAMENTO
from dataclasses import asdict

class ProcessadorDados:
    @staticmethod
    def _converter_para_float(valor_str):
        if not valor_str or valor_str == 'N/A':
            return 0.0
        try:
            limpo = str(valor_str).replace('.', '').replace(',', '.')
            return float(limpo)
        except ValueError:
            return 0.0

    @staticmethod
    def _extrair_codigo_ficha(texto_ficha):
        match = re.search(r'\((\d+)\)', str(texto_ficha))
        return match.group(1) if match else 'Sem Ficha'

    @staticmethod
    def preparar_dataframe_faturas(faturas_lidas: list, mapa_fichas: dict, headers: dict, coluna_id: str) -> pd.DataFrame:
        faturas_dicts = [asdict(f) for f in faturas_lidas]
        df = pd.DataFrame(faturas_dicts)
        
        df['ficha'] = df[coluna_id].map(mapa_fichas).fillna('Sem Ficha')        
        df = df[list(headers.keys())]
        df = ProcessadorDados.ordenar_por_id(df, coluna_id)
        return df.rename(columns=headers)

    @staticmethod
    def gerar_relatorio_final(faturas_lidas: list, mapa_fichas: dict, coluna_id: str) -> pd.DataFrame:
        faturas_dicts = [asdict(f) for f in faturas_lidas]
        df = pd.DataFrame(faturas_dicts)

        df['Valor Líquido'] = df['valor'].apply(ProcessadorDados._converter_para_float)
        df['IR'] = df['retencao_ir'].apply(ProcessadorDados._converter_para_float)
        df['Valor Bruto'] = df['Valor Líquido'] + df['IR']
        
        df['ficha_extensa'] = df[coluna_id].map(mapa_fichas).fillna('Sem Ficha')
        df['AÇÃO'] = df['ficha_extensa'].apply(ProcessadorDados._extrair_codigo_ficha)

        df_agrupado = df.groupby('AÇÃO').agg({
            'Valor Líquido': 'sum',
            'IR': 'sum',
            'Valor Bruto': 'sum'
        }).reset_index()

        df_agrupado['DOTAÇÃO'] = DOTACAO_FIXA
        df_agrupado['SECRETARIA RESPONSAVEL'] = df_agrupado['AÇÃO'].apply(
            lambda x: RELACAO_FICHAS_ORCAMENTO.get(x, {}).get('secretaria', '')
        )
        df_agrupado['EMPENHO'] = df_agrupado['AÇÃO'].apply(
            lambda x: RELACAO_FICHAS_ORCAMENTO.get(x, {}).get('empenho', '')
        )
        df_agrupado['AF'] = df_agrupado['AÇÃO'].apply(
            lambda x: RELACAO_FICHAS_ORCAMENTO.get(x, {}).get('af', '')
        )

        colunas = [
            'DOTAÇÃO', 'AÇÃO', 'SECRETARIA RESPONSAVEL', 
            'EMPENHO', 'AF', 'Valor Líquido', 'IR', 'Valor Bruto'
        ]
        df_final = df_agrupado[colunas].copy()

        for col in ['Valor Líquido', 'IR', 'Valor Bruto']:
            df_final[col] = df_final[col].map(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))

        return df_final

    @staticmethod
    def ordenar_por_id(df: pd.DataFrame, coluna_id: str) -> pd.DataFrame:
        if coluna_id == 'rgi':
            df[coluna_id] = pd.Categorical(df[coluna_id], categories=RGI_SABESP, ordered=True)
        elif coluna_id == 'uc':
            df[coluna_id] = pd.Categorical(df[coluna_id], categories=UC_EDP, ordered=True)
        return df.sort_values(coluna_id)
