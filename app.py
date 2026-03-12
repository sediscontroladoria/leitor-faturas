from services.executar_leitura import executar_leitura
from services.executar_separacao import executar_separacao

if __name__ == '__main__':
    UPLOADS = './uploads'
    DATA_DIR = './data'
    PLANILHA_EXTERNA = 'relacao_faturas.xlsx'

    executar_leitura(diretorio_entrada=UPLOADS, diretorio_saida=DATA_DIR)
    executar_separacao(planilha_path=PLANILHA_EXTERNA, diretorio_uploads=UPLOADS, pasta_saida_zip=DATA_DIR)