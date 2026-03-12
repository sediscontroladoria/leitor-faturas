import streamlit as st
import os
import tempfile
from services.factory import ServiceFactory
from services.organizador_faturas import OrganizadorFaturas
from components.widgets import (
    render_page_header, select_concessionaria, upload_faturas_pdf, 
    upload_planilha_relacao, ProgressTracker, render_download_section
)

def separador_faturas():
    render_page_header('Separador de Faturas', '📂')

    tipo_fatura = select_concessionaria('separador_concess')

    col1, col2 = st.columns(2)

    with col1:
        planilha_file = upload_planilha_relacao()        
    with col2:
        arquivos_pdf = upload_faturas_pdf()

    if planilha_file and arquivos_pdf and st.button('Separar e Organizar'):
        separador = ServiceFactory.get_separador(tipo_fatura)
        
        if separador:
            with tempfile.TemporaryDirectory() as pasta_trabalho:
                pasta_uploads = os.path.join(pasta_trabalho, 'uploads')
                pasta_separadas = os.path.join(pasta_trabalho, 'separadas')
                pasta_organizadas = os.path.join(pasta_trabalho, 'organizadas')
                os.makedirs(pasta_uploads)
                
                for pdf in arquivos_pdf:
                    with open(os.path.join(pasta_uploads, pdf.name), 'wb') as f:
                        f.write(pdf.getbuffer())
                
                planilha_path = os.path.join(pasta_trabalho, 'relacao.xlsx')
                with open(planilha_path, 'wb') as f:
                    f.write(planilha_file.getbuffer())

                tracker = ProgressTracker()
                try:
                    tracker.text.info('Separando PDFs...')
                    caminhos_pdfs = [os.path.join(pasta_uploads, f) for f in os.listdir(pasta_uploads)]
                    separador.separar(caminhos_pdfs, pasta_separadas)
                    
                    tracker.bar.progress(60)
                    tracker.text.info('Organizando pastas por ficha...')
                    organizador = OrganizadorFaturas()
                    organizador.agrupar_por_planilha(planilha_path, pasta_separadas, pasta_organizadas)
                    
                    tracker.bar.progress(90)
                    zip_path_base = os.path.join(pasta_trabalho, f'Faturas_{tipo_fatura}')
                    caminho_zip = organizador.compactar_saida(pasta_organizadas, zip_path_base)
                    
                    tracker.clear()
                    with open(caminho_zip, 'rb') as f:
                        render_download_section(
                            label='⬇️ Baixar Faturas Organizadas (ZIP)',
                            data=f.read(),
                            file_name=f'Organizadas_{tipo_fatura}.zip',
                            mime='application/zip'
                        )
                except Exception as e:
                    st.error(f'Erro no processamento: {e}')
        else:
            st.warning(f'Separador para {tipo_fatura} em desenvolvimento.')

if __name__ == '__main__':
    separador_faturas()