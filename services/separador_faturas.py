import os
import re
from pypdf import PdfReader, PdfWriter
from utils.regex_patterns import sabesp_patterns

class SeparadorFaturas():
    def __init__(self):
        self.pattern_id = sabesp_patterns['num_documento']

    def separar(self, pdf_paths, pasta_saida):
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)

        faturas_processadas = []

        for pdf_path in pdf_paths:
            reader = PdfReader(pdf_path)
            writer = None
            documento_atual = None

            for page in reader.pages:
                texto = page.extract_text()
                match = re.search(self.pattern_id, texto)

                if match:
                    if writer and documento_atual:
                        self._salvar_fatura(writer, documento_atual, pasta_saida)
                    
                    documento_atual = match.group(1)
                    writer = PdfWriter()
                    writer.add_page(page)
                    faturas_processadas.append(documento_atual)
                elif writer:
                    writer.add_page(page)

            if writer and documento_atual:
                self._salvar_fatura(writer, documento_atual, pasta_saida)

        return faturas_processadas

    def _salvar_fatura(self, writer, doc_id, pasta_saida):
        caminho_final = os.path.join(pasta_saida, f'{doc_id}.pdf')
        with open(caminho_final, 'wb') as f:
            writer.write(f)