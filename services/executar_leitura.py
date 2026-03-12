import datetime
from services.leitor_sabesp import LeitorSabesp

def executar_leitura(diretorio_entrada='./uploads', diretorio_saida='./data'):
    leitor = LeitorSabesp() 
    data_atual = datetime.date.today().strftime('%Y-%m-%d')
    nome_arquivo = f'Faturas-Sabesp-{data_atual}.csv'
    
    headers_sabesp = {
        'num_documento': 'Nº Documento',
        'rgi': 'RGI',
        'hidrometro': 'Hidrômetro',
        'vencimento': 'Vencimento',
        'valor': 'Valor (R$)',
        'consumo': 'Consumo (m³)',
        'retencao_ir': 'Retenção IR'
    }

    print(f'Iniciando extração de dados em: {diretorio_entrada}...')
    faturas = leitor.processar_diretorio(diretorio_entrada)
    
    if faturas:
        leitor.exportar_planilha(faturas, diretorio_saida, nome_arquivo, headers=headers_sabesp)
        return True
    
    print('Nenhuma fatura encontrada para leitura.')
    return False