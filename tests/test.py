import pdfplumber
import re
import os

PATH = 'C:/Users/Informática/Desktop/Eduarda/Projects/leitor-sedis/tests/samples'

def extract(file_name):
    with pdfplumber.open(f'{PATH}/{file_name}.pdf') as pdf:
        return ' '.join([p.extract_text(x_tolerance=3) or '' for p in pdf.pages])

def ver_raw_text(file_name):
    """Mostra o texto bruto de um arquivo específico."""
    print(f"\n--- RAW TEXT: {file_name} ---\n")
    print(extract(file_name))
    print("\n" + "-"*30)

def listar_dados():
    patterns = {
        "Fatura":  r"\d{27}(\d{7})",
        "UC":      r"(\d[\d.]{5,}-\d{2})",
        "Medidor": r"MEDIDOR:\s*0*(\d+)",
        "Data":    r"(?:MEDIDOR:|CEP:)\s*.*?\s*(\d{2}/\d{2}/\d{4})",
        "Total":   r"(?:(?:\d{2}/\d{2}/\d{4})\s+|TOTAL\s+)([\d.\s]+,\s*[\d\s]+)",
        "Consumo": r"Consumo kWh\s*(\d+[\s\d]*),\d+",
        "IR":      r"Retenção Imposto de Renda\s*(\d+,\d+\s*\d+)"
    }

    arquivos = [f.replace('.pdf', '') for f in os.listdir(PATH) if f.endswith('.pdf')]
    
    for arquivo in arquivos:
        texto = extract(arquivo)
        print(f"\n📄 Arquivo: {arquivo}")
        
        for rotulo, regex in patterns.items():
            match = re.search(regex, texto)
            if match:
                valor = match.group(1).replace(" ", "")
                
                if rotulo == "UC":
                    valor = valor.replace(".", "").replace("-", "").lstrip("0")
                
                print(f"  {rotulo.ljust(8)}: {valor}")
            else:
                print(f"  {rotulo.ljust(8)}: Não encontrado")

listar_dados()