import datetime
from core.leitor_sabesp import LeitorSabesp
from utils.generate_sheet import generate_sheet

if __name__ == '__main__':
    DATA_ATUAL = datetime.date.today().strftime('%Y-%m-%d')
    pdf_dir = './uploads'
    csv_dir = './data'
    csv_filename = f'Faturas-Sabesp-{DATA_ATUAL}.csv'
    
    leitor = LeitorSabesp() 
    
    print(f'Iniciando processamento em: {pdf_dir}...')
    faturas = leitor.processar_diretorio(pdf_dir)
    
    if faturas:
        generate_sheet(faturas, csv_dir, csv_filename)
    else:
        print('Nenhuma fatura encontrada.')