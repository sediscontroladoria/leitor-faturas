import streamlit as st
import io
import os
import tempfile

from utils.headers import sabesp_headers, edp_headers
from utils.constants import RGI_FICHA_SABESP, UC_FICHA_EDP 
from services.factory import ServiceFactory
from services.processador_dados import ProcessadorDados
from services.organizador_faturas import OrganizadorFaturas

from components.widgets import (
    render_page_header, select_concessionaria, 
    upload_faturas_pdf, ProgressTracker, render_download_section,
    select_mes_competencia, input_ano, select_tipo_debito,
    select_conta, input_complemento
)

if 'dados_csv' not in st.session_state:
    st.session_state.dados_csv = None
if 'dados_zip' not in st.session_state:
    st.session_state.dados_zip = None
if 'dados_relatorio' not in st.session_state:
    st.session_state.dados_relatorio = None
if 'processado' not in st.session_state:
    st.session_state.processado = False

render_page_header('Processador de Faturas', '📄')

tipo_fatura = select_concessionaria('leitor_concess')

if tipo_fatura == 'Sabesp':
    mapa_fichas_atual = RGI_FICHA_SABESP
    headers_atuais = sabesp_headers
    coluna_id_atual = 'rgi'
else:
    mapa_fichas_atual = UC_FICHA_EDP 
    headers_atuais = edp_headers
    coluna_id_atual = 'uc'

col_mes, col_ano = st.columns(2)
with col_mes:
    mes_comp = select_mes_competencia('mes_comp')
with col_ano:
    ano_comp = input_ano('ano_comp')

col_deb, col_conta = st.columns(2)
with col_deb:
    tipo_debito = select_tipo_debito('tipo_debito')
with col_conta:
    conta_fatura = select_conta('conta_fatura')

complemento = input_complemento('complemento')

arquivos_pdf = upload_faturas_pdf()

if arquivos_pdf and st.button('Processar Faturas'):
    leitor = ServiceFactory.get_leitor(tipo_fatura)
    separador = ServiceFactory.get_separador()
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
                        mapa_fichas_atual
                    )

                    tracker.text.info('Preparando planilha de dados...')
                    df_final = ProcessadorDados.preparar_dataframe_faturas(
                        faturas_lidas, 
                        mapa_fichas_atual, 
                        headers_atuais,
                        coluna_id_atual
                    )

                    tracker.text.info('Gerando relatório final...')
                    df_relatorio = ProcessadorDados.gerar_relatorio_final(
                        faturas_lidas,
                        mapa_fichas_atual,
                        coluna_id_atual
                    )

                    tracker.bar.progress(90)
                    tracker.text.info('Gerando arquivos de saída...')
                    
                    csv_buffer = io.StringIO()
                    df_final.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8-sig')
                    st.session_state.dados_csv = csv_buffer.getvalue().encode('utf-8-sig')
                    
                    def fmt_br(v): 
                        return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

                    vl_total = sum(ProcessadorDados._converter_para_float(f.valor) for f in faturas_lidas)
                    ir_total = sum(ProcessadorDados._converter_para_float(f.retencao_ir) for f in faturas_lidas)
                    vb_total = vl_total + ir_total

                    rel_buffer = io.StringIO()
                    venc_ref = faturas_lidas[0].vencimento if faturas_lidas else 'N/A'
                    rel_buffer.write(f'Relatório das faturas {tipo_fatura} referentes a {mes_comp}/{ano_comp};;;;;;;\n')
                    rel_buffer.write(f'{tipo_debito} - {conta_fatura} - Vencimento {venc_ref} - {complemento};;;;;;;\n')
                    df_relatorio.to_csv(rel_buffer, index=False, sep=';', encoding='utf-8-sig')
                    rel_buffer.write(f'Total Geral;;;;;{fmt_br(vl_total)};{fmt_br(ir_total)};{fmt_br(vb_total)}')
                    st.session_state.dados_relatorio = rel_buffer.getvalue().encode('utf-8-sig')
                    
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
    st.success('Processamento concluído! Faça o download de seus arquivos abaixo:')
    
    c1, c2, c3 = st.columns([1, 1.2, 1.2]) 
    
    with c1:
        render_download_section(1, 'Baixar Planilha (.CSV)', st.session_state.dados_csv, f'Planilha_{tipo_fatura}', 'text/csv')
    
    with c2:
        render_download_section(2, 'Baixar Faturas (.ZIP)', st.session_state.dados_zip, f'Faturas_{tipo_fatura}', 'application/zip')

    with c3:
        render_download_section(3, 'Baixar Relatório Final (.CSV)', st.session_state.dados_relatorio, f'Relatorio_Final_{tipo_fatura}', 'text/csv')