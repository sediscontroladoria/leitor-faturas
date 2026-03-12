import streamlit as st
import pandas as pd
import io

from dataclasses import asdict
from utils.headers import sabesp_headers
from services.factory import ServiceFactory

from components.widgets import (
    render_page_header, select_concessionaria, 
    upload_faturas_pdf, ProgressTracker, render_download_section
)

def leitor_faturas():
    render_page_header('Leitor de Faturas', '📄')

    tipo_fatura = select_concessionaria('leitor_concess')
    arquivos_pdf = upload_faturas_pdf()

    if arquivos_pdf and st.button('Gerar Planilha'):
        leitor = ServiceFactory.get_leitor(tipo_fatura)
        
        if leitor:
            faturas_data = []
            tracker = ProgressTracker()

            for i, pdf_file in enumerate(arquivos_pdf):
                tracker.update(i, len(arquivos_pdf), pdf_file.name)
                fatura = leitor.processar(pdf_file)
                faturas_data.append(asdict(fatura))

            if faturas_data:
                df = pd.DataFrame(faturas_data)
                df.rename(columns=sabesp_headers, inplace=True)

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8-sig')
                
                render_download_section(
                    label='⬇️ Baixar Planilha CSV',
                    data=csv_buffer.getvalue(),
                    file_name=f'Faturas_{tipo_fatura}.csv',
                    mime='text/csv'
                )
        else:
            st.error(f'O leitor para {tipo_fatura} ainda não foi implementado.')

if __name__ == '__main__':
    leitor_faturas()