import pdfplumber
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FOLDER_PATH = BASE_DIR / 'samples' 

def extract(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return ' '.join([p.extract_text(x_tolerance=3) or '' for p in pdf.pages])

def raw_text(pdf_path):
    print(f'\n--- RAW TEXT: {pdf_path.name} ---\n')
    print(extract(pdf_path))
    print('\n' + '-'*30)

def listar_dados():  
    patterns = {
        'Fatura':  r'\d{27}(\d{7})',
        'UC':      r'(\d[\d.]{5,}-\d{2})',
        'Medidor': r'MEDIDOR:\s*0*(\d+)',
        'Data':    r'(?:MEDIDOR:|CEP:)\s*.*?\s*(\d{2}/\d{2}/\d{4})',
        'Total':   r'(?:(?:\d{2}/\d{2}/\d{4})\s+|TOTAL\s+)([\d.\s]+,\s*\d{2})',
        'Consumo': r'Consumo kWh\s*(\d+[\s\d]*),\d+',
        'IR':      r'Retenção Imposto de Renda\s+(?:\d+,\d{4}\s+)?(\d+[\s\d]*,[\s\d]+)'
    }

    if not FOLDER_PATH.exists():
        print(f'Erro: A pasta de amostras não foi encontrada em: {FOLDER_PATH}')
        return

    arquivos_pdf = list(FOLDER_PATH.glob('*.pdf'))
    
    if not arquivos_pdf:
        print(f'Nenhum arquivo PDF encontrado em: {FOLDER_PATH}')
        return

    for pdf_path in arquivos_pdf:
        texto = extract(pdf_path)
        print(f'\n📄 Arquivo: {pdf_path.name}')
        
        for rotulo, regex in patterns.items():
            match = re.search(regex, texto)
            if match:
                valor = match.group(1).replace(' ', '')
                
                if rotulo == 'UC':
                    valor = valor.replace('.', '').replace('-', '').lstrip('0')
                
                print(f'  {rotulo.ljust(8)}: {valor}')
            else:
                print(f'  {rotulo.ljust(8)}: Não encontrado')

FILE_PATH = BASE_DIR / 'samples' / '11785002.pdf'

if __name__ == '__main__':
    listar_dados()