import pdfplumber
import re
import os

from abc import ABC

from models.fatura_sabesp import FaturaSabesp
from utils.regex_patterns import sabesp_patterns

class LeitorFaturas():
    def __init__(self):
        self.pdf_content = ''

    def _extrair_texto(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            return ' '.join([p.extract_text(x_tolerance=3) or '' for p in pdf.pages])
    
    def processar_sabesp(self, pdf_path):
        texto = self._extrair_texto(pdf_path)
        
        def get_match(pattern_key):
            match = re.search(sabesp_patterns[pattern_key], texto)
            return match.group(1) if match else 'N/A'
        
        return FaturaSabesp(
            num_documento=get_match('num_documento'),
            rgi=get_match('rgi'),
            hidrometro=get_match('hidrometro'),
            valor=get_match('valor'),
            consumo=get_match('consumo'),
            vencimento=get_match('vencimento'),
            debito_automatico='SIM' if 'DÉBITO AUTOMÁTICO' in texto else 'NÃO',
            retencao_ir=get_match('retencao_ir'),
        )
    
    def processar_faturas(self, diretorio_path, opt=0):
        faturas = []

        if not os.path.exists(diretorio_path):
            print(f'Erro: O diretório "{diretorio_path}" não existe.')
            return faturas

        for file in os.listdir(diretorio_path):
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(diretorio_path, file)
                
                fatura = self.processar_sabesp(full_path) if opt == 0 else self.processar_edp(full_path)
                faturas.append(fatura)

        return faturas