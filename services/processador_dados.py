import pandas as pd
import re
from utils.constants import RGI_SABESP, DOTACAO_FIXA, RELACAO_FICHAS_ORCAMENTO
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
    def preparar_dataframe_faturas(faturas_lidas: list, mapa_rgi_ficha: dict, headers: dict) -> pd.DataFrame:
        faturas_dicts = [asdict(f) for f in faturas_lidas]
        df = pd.DataFrame(faturas_dicts)
        df['ficha'] = df['rgi'].map(mapa_rgi_ficha).fillna('Sem Ficha')
        df = ProcessadorDados.ordenar_por_rgi(df)
        return df.rename(columns=headers)

    @staticmethod
    def gerar_relatorio_final(faturas_lidas: list, mapa_rgi_ficha: dict) -> pd.DataFrame:
        faturas_dicts = [asdict(f) for f in faturas_lidas]
        df = pd.DataFrame(faturas_dicts)

        df['Valor Líquido'] = df['valor'].apply(ProcessadorDados._converter_para_float)
        df['IR'] = df['retencao_ir'].apply(ProcessadorDados._converter_para_float)
        df['Valor Bruto'] = df['Valor Líquido'] + df['IR']
        
        df['ficha_extensa'] = df['rgi'].map(mapa_rgi_ficha).fillna('Sem Ficha')
        df['AÇÃO'] = df['ficha_extensa'].apply(ProcessadorDados._extrair_codigo_ficha)

        # AGRUPAMENTO POR AÇÃO (FICHA)
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
    def ordenar_por_rgi(df: pd.DataFrame, coluna_rgi: str = 'rgi') -> pd.DataFrame:
        df[coluna_rgi] = pd.Categorical(df[coluna_rgi], categories=RGI_SABESP, ordered=True)
        return df.sort_values(coluna_rgi)