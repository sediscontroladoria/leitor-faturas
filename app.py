import datetime
from services.leitor_sabesp import LeitorSabesp
from utils.generate_sheet import generate_sheet

CURRENT_DATE = datetime.date.today().strftime('%Y-%m-%d')
CSV_FILENAME = f'Faturas-Sabesp-{CURRENT_DATE}.csv'

PDF_DIR = './uploads'
CSV_DIR = './data'
    
if __name__ == '__main__':        
    leitor = LeitorSabesp() 
    
    print(f'Analisando os arquivos em: {PDF_DIR}...')
        
    faturas = leitor.processar_diretorio(PDF_DIR)
    
    if faturas:
        generate_sheet(faturas, CSV_DIR, CSV_FILENAME)
    else:
        print('Nenhuma fatura encontrada.')