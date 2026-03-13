import streamlit as st
import io
import os
import tempfile

from utils.headers import sabesp_headers
from utils.constants import RGI_FICHA_SABESP 
from services.factory import ServiceFactory
from services.processador_dados import ProcessadorDados
from services.organizador_faturas import OrganizadorFaturas

from components.widgets import (
    render_page_header, select_concessionaria, 
    upload_faturas_pdf, ProgressTracker, render_download_section
)

if 'dados_csv' not in st.session_state:
    st.session_state.dados_csv = None
if 'dados_zip' not in st.session_state:
    st.session_state.dados_zip = None
if 'processado' not in st.session_state:
    st.session_state.processado = False

render_page_header('Processador de Faturas', '📄')

tipo_fatura = select_concessionaria('leitor_concess')
arquivos_pdf = upload_faturas_pdf()

if arquivos_pdf and st.button('Processar Faturas'):
    leitor = ServiceFactory.get_leitor(tipo_fatura)
    separador = ServiceFactory.get_separador(tipo_fatura)
    organizador = OrganizadorFaturas()
    
    if leitor and separador:
        tracker = ProgressTracker()
        
        try:
            with tempfile.TemporaryDirectory() as pasta_trabalho:
                pasta_uploads = os.path.join(pasta_trabalho, 'uploads')
                pasta_separadas = os.path.join(pasta_trabalho, 'separadas')
                pasta_organizadas = os.path.join(pasta_trabalho, 'organizadas')
                os.makedirs(pasta_uploads)
                
                caminhos_pdfs = []
                for pdf in arquivos_pdf:
                    caminho = os.path.join(pasta_uploads, pdf.name)
                    with open(caminho, 'wb') as f:
                        f.write(pdf.getbuffer())
                    caminhos_pdfs.append(caminho)

                faturas_lidas = []
                tracker.text.info('Lendo faturas e extraindo dados...')
                for i, caminho_pdf in enumerate(caminhos_pdfs):
                    tracker.update(i, len(caminhos_pdfs), os.path.basename(caminho_pdf))
                    fatura = leitor.processar(caminho_pdf)
                    faturas_lidas.append(fatura)

                if faturas_lidas:
                    tracker.bar.progress(50)
                    tracker.text.info('Separando páginas de PDFs...')
                    separador.separar(caminhos_pdfs, pasta_separadas)

                    tracker.bar.progress(75)
                    tracker.text.info('Organizando faturas por Ficha...')
                    organizador.agrupar_por_mapeamento(
                        faturas_lidas, 
                        pasta_separadas, 
                        pasta_organizadas, 
                        RGI_FICHA_SABESP
                    )

                    tracker.text.info('Preparando planilha de dados...')
                    df_final = ProcessadorDados.preparar_dataframe_faturas(
                        faturas_lidas, 
                        RGI_FICHA_SABESP, 
                        sabesp_headers
                    )

                    tracker.bar.progress(90)
                    tracker.text.info('Gerando ficheiros de saída...')
                    
                    csv_buffer = io.StringIO()
                    df_final.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8-sig')
                    st.session_state.dados_csv = csv_buffer.getvalue().encode('utf-8-sig')
                    
                    zip_path_base = os.path.join(pasta_trabalho, f'Faturas_Organizadas_{tipo_fatura}')
                    caminho_zip = organizador.compactar_saida(pasta_organizadas, zip_path_base)
                    with open(caminho_zip, 'rb') as f:
                        st.session_state.dados_zip = f.read()
                    
                    st.session_state.processado = True
                    tracker.clear()
                else:
                    st.warning('Nenhuma fatura pôde ser lida.')

        except Exception as e:
            tracker.clear()
            st.error(f'Falha no processamento: {str(e)}')
            st.session_state.processado = False
    else:
        st.error(f'Ferramentas para {tipo_fatura} ainda não implementadas.')

if st.session_state.processado:
    st.success('Processamento concluído! Descarregue os seus ficheiros abaixo:')
    
    col1, col2, col3 = st.columns([1, 1.4, 3]) 
    
    with col1:
        render_download_section(
            option=1,
            label='Baixar Planilha (.CSV)',
            data=st.session_state.dados_csv,
            file_name=f'Planilha_{tipo_fatura}',
            mime='text/csv'
        )
    
    with col2:
        render_download_section(
            option=2,
            label='Baixar Faturas Organizadas (.ZIP)',
            data=st.session_state.dados_zip,
            file_name=f'Faturas_{tipo_fatura}',
            mime='application/zip'
        )