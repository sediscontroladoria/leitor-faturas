import streamlit as st
from utils.headers import sabesp_headers, edp_headers
from utils.constants import RGI_FICHA_SABESP, UC_FICHA_EDP 
from services.orquestrador_faturas import OrquestradorFaturas

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
    tracker = ProgressTracker()
    try:
        resultados = OrquestradorFaturas.processar_lote(
            arquivos_pdf, tipo_fatura, mes_comp, ano_comp,
            tipo_debito, conta_fatura, complemento,
            mapa_fichas_atual, headers_atuais, coluna_id_atual,
            tracker
        )
        
        if resultados:
            st.session_state.dados_csv = resultados['csv']
            st.session_state.dados_relatorio = resultados['relatorio']
            st.session_state.dados_zip = resultados['zip']
            st.session_state.processado = True
            tracker.clear()
        else:
            st.warning('Nenhuma fatura pôde ser lida.')
            
    except Exception as e:
        tracker.clear()
        st.error(f'Falha no processamento: {str(e)}')

if st.session_state.processado:
    st.success('Processamento concluído! Faça o download de seus arquivos abaixo:')
    
    c1, c2, c3 = st.columns([1, 1.2, 1.2]) 
    
    with c1:
        render_download_section(1, 'Baixar Planilha (.CSV)', st.session_state.dados_csv, f'Planilha_{tipo_fatura}', 'text/csv')
    
    with c2:
        render_download_section(2, 'Baixar Faturas (.ZIP)', st.session_state.dados_zip, f'Faturas_{tipo_fatura}', 'application/zip')

    with c3:
        render_download_section(3, 'Baixar Relatório Final (.CSV)', st.session_state.dados_relatorio, f'Relatorio_Final_{tipo_fatura}', 'text/csv')
