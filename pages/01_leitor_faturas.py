import streamlit as st
from utils.headers import sabesp_headers, edp_headers
from utils.constants import RGI_FICHA_SABESP, UC_FICHA_EDP 
from services.orquestrador_faturas import OrquestradorFaturas

from components.widgets import (
    render_page_header, select_concessionaria, 
    upload_faturas_pdf, ProgressTracker, render_download_section,
    select_mes_competencia, input_ano, select_tipo_debito,
    select_conta, input_complemento, select_opcoes_processamento
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

col_deb, col_opcoes = st.columns(2)
with col_deb:
    tipo_debito = select_tipo_debito('tipo_debito')
with col_opcoes:
    opcoes_saida = select_opcoes_processamento('opcoes_saida')

col_conta, col_comp = st.columns(2)
with col_conta:
    conta_fatura = select_conta('conta_fatura')
with col_comp:
    complemento = input_complemento('complemento')

arquivos_pdf = upload_faturas_pdf()

if arquivos_pdf and st.button('Processar Faturas'):
    if not opcoes_saida:
        st.error('Selecione ao menos um item para gerar.')
    else:
        tracker = ProgressTracker()
        try:
            resultados = OrquestradorFaturas.processar_lote(
                arquivos_pdf, tipo_fatura, mes_comp, ano_comp,
                tipo_debito, conta_fatura, complemento,
                mapa_fichas_atual, headers_atuais, coluna_id_atual,
                opcoes_saida, tracker
            )
            
            if resultados:
                st.session_state.dados_csv = resultados.get('csv')
                st.session_state.dados_relatorio = resultados.get('relatorio')
                st.session_state.dados_zip = resultados.get('zip')
                st.session_state.processado = True
                tracker.clear()
            else:
                st.warning('Nenhuma fatura pôde ser lida com os critérios selecionados.')
                
        except Exception as e:
            tracker.clear()
            st.error(f'Falha no processamento: {str(e)}')

if st.session_state.processado:
    st.success('Processamento concluído! Faça o download de seus arquivos abaixo:')
    
    cols_existentes = [opt for opt in ['Gerar Planilha', 'Gerar ZIP', 'Gerar Relatório Final'] if opt in opcoes_saida]
    cols = st.columns(len(cols_existentes)) 
    
    idx = 0
    if 'Gerar Planilha' in opcoes_saida and st.session_state.dados_csv:
        with cols[idx]:
            render_download_section(1, 'Baixar Planilha (.CSV)', st.session_state.dados_csv, f'Planilha_{tipo_fatura}', 'text/csv')
        idx += 1
    
    if 'Gerar ZIP' in opcoes_saida and st.session_state.dados_zip:
        with cols[idx]:
            render_download_section(2, 'Baixar Faturas (.ZIP)', st.session_state.dados_zip, f'Faturas_{tipo_fatura}', 'application/zip')
        idx += 1

    if 'Gerar Relatório Final' in opcoes_saida and st.session_state.dados_relatorio:
        with cols[idx]:
            render_download_section(3, 'Baixar Relatório Final (.CSV)', st.session_state.dados_relatorio, f'Relatorio_Final_{tipo_fatura}', 'text/csv')