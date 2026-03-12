import os
import shutil
import pandas as pd

COL_FATURA = 'N° da Fatura'
COL_FICHA = 'Ficha(Ação)'

class OrganizadorFaturas:
    @staticmethod
    def agrupar_por_planilha(planilha_path, pasta_origem, pasta_destino):
        df = pd.read_excel(planilha_path)
        
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        erros = []
        for _, linha in df.iterrows():
            num_fatura = str(linha[COL_FATURA]).strip()
            ficha = str(linha[COL_FICHA]).strip()
            
            origem = os.path.join(pasta_origem, f'{num_fatura}.pdf')
            subpasta = os.path.join(pasta_destino, ficha)
            
            if os.path.exists(origem):
                os.makedirs(subpasta, exist_ok=True)
                shutil.move(origem, os.path.join(subpasta, f'{num_fatura}.pdf'))
            else:
                erros.append(num_fatura)
        
        return erros

    @staticmethod
    def compactar_saida(pasta_para_zip, nome_arquivo):
        shutil.make_archive(nome_arquivo, 'zip', pasta_para_zip)
        return f'{nome_arquivo}.zip'