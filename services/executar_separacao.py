import os
import shutil
from services.separador_sabesp import SeparadorSabesp
from services.organizador_faturas import OrganizadorFaturas

def executar_separacao(planilha_path, diretorio_uploads='./uploads', pasta_saida_zip='./data'):
    pasta_temp = './temp_faturas'
    pasta_agrupadas = './faturas_organizadas'
    zip_path_base = os.path.join(pasta_saida_zip, 'Faturas_Separadas_Organizadas')

    arquivos_pdf = [os.path.join(diretorio_uploads, f) for f in os.listdir(diretorio_uploads) if f.endswith('.pdf')]
    
    if not arquivos_pdf:
        print('Erro: Nenhum PDF encontrado para separação.')
        return False

    try:
        separador = SeparadorSabesp()
        separador.separar(arquivos_pdf, pasta_temp)

        organizador = OrganizadorFaturas()

        organizador.agrupar_por_planilha(planilha_path, pasta_temp, pasta_agrupadas)

        print(f'Gerando arquivo ZIP em {pasta_saida_zip}...')
        caminho_final_zip = organizador.compactar_saida(pasta_agrupadas, zip_path_base)
        
        print(f'Sucesso! Arquivo gerado: {caminho_final_zip}')
        return True

    finally:
        if os.path.exists(pasta_temp):
            shutil.rmtree(pasta_temp)
        if os.path.exists(pasta_agrupadas):
            shutil.rmtree(pasta_agrupadas)