import pdfplumber
import re
import os
from abc import ABC, abstractmethod

class Leitor(ABC):
    def _extrair_texto(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            return ' '.join([p.extract_text(x_tolerance=3) or '' for p in pdf.pages])

    def _get_match(self, pattern, texto):
        match = re.search(pattern, texto)
        return match.group(1) if match else 'N/A'

    @abstractmethod
    def processar(self, pdf_path):
        pass

    def processar_diretorio(self, diretorio_path):
        faturas = []
        if not os.path.exists(diretorio_path):
            print(f'Erro: O diretório "{diretorio_path}" não existe.')
            return faturas

        for file in os.listdir(diretorio_path):
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(diretorio_path, file)
                faturas.append(self.processar(full_path))
        return faturas