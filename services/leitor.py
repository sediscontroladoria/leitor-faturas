import pdfplumber
import re
import os

from abc import ABC, abstractmethod
from dataclasses import asdict
from pandas import DataFrame
from pathlib import Path

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
    
    def exportar_planilha(self, faturas_list, folder_path, filename, headers=None):
        """Gera a planilha CSV a partir da lista de faturas processadas."""
        output_dir = Path(folder_path)    
        output_dir.mkdir(parents=True, exist_ok=True)
        final_path = output_dir / filename
        
        data = [asdict(f) for f in faturas_list]
        df = DataFrame(data)
        
        if headers:
            df.columns = [headers.get(col, col.replace('_', ' ').title()) for col in df.columns]
        
        df.to_csv(
            final_path, 
            index=False, 
            encoding='utf-8-sig', 
            sep=';', 
            decimal=','
        )    
        
        print(f'\nPlanilha "{filename}" gerada com sucesso em: {output_dir.absolute()}')