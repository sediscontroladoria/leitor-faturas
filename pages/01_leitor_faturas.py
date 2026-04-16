import streamlit as st
from services.orquestrador_faturas import OrquestradorFaturas
from services.factory import ServiceFactory

from components.widgets import (
    render_page_header, select_centro_comunitario, select_concessionaria, 
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

col_tipo, col_centro = st.columns(2)
with col_tipo:
    tipo_fatura = select_concessionaria('leitor_concess')
with col_centro:
    centro_comunitario = select_centro_comunitario('cen_comun')

is_centro = centro_comunitario == 'Sim'
config_fatura = ServiceFactory.get_configuracao_fatura(tipo_fatura, is_centro)

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

nomes_arquivos = tuple([f.name for f in arquivos_pdf]) if arquivos_pdf else ()

estado_atual = (
    tipo_fatura, centro_comunitario, mes_comp, ano_comp, 
    tipo_debito, tuple(opcoes_saida), conta_fatura, complemento,
    nomes_arquivos
)

if estado_atual != st.session_state.estado_anterior:
    st.session_state.processado = False
    st.session_state.dados_csv = None
    st.session_state.dados_zip = None
    st.session_state.dados_relatorio = None
    st.session_state.estado_anterior = estado_atual
    
if arquivos_pdf and st.button('Processar Faturas'):
    if not opcoes_saida:
        st.error('Selecione ao menos um item para gerar.')
    else:
        tracker = ProgressTracker()
        try:
            resultados = OrquestradorFaturas.processar_lote(
                arquivos_pdf=arquivos_pdf, 
                tipo_fatura=tipo_fatura, 
                mes_comp=mes_comp, 
                ano_comp=ano_comp,
                tipo_debito=tipo_debito, 
                conta_fatura=conta_fatura, 
                complemento=complemento,
                opcoes_saida=opcoes_saida, 
                config_fatura=config_fatura,
                tracker=tracker
            )
            
            if resultados:
                st.session_state.dados_csv = resultados.get('csv')
                st.session_state.dados_relatorio = resultados.get('relatorio')
                st.session_state.dados_zip = resultados.get('zip')
                st.session_state.processado = True
                tracker.clear()
            else:
                st.session_state.processado = False
                st.session_state.dados_csv = None
                st.session_state.dados_relatorio = None
                st.session_state.dados_zip = None
                st.warning('Nenhuma fatura pôde ser lida com os critérios selecionados.')
                
        except Exception as e:
            tracker.clear()
            st.error(f'Falha no processamento: {str(e)}')

if st.session_state.processado:
    cols_existentes = [opt for opt in ['Gerar Planilha', 'Gerar ZIP', 'Gerar Relatório Final'] if opt in opcoes_saida]
    
    if cols_existentes:
        st.success('Processamento concluído! Faça o download de seus arquivos abaixo:')
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
                render_download_section(
                    3, 
                    'Baixar Relatório Final (.XLSX)', 
                    st.session_state.dados_relatorio, 
                    f'Relatorio_Final_{tipo_fatura}', 
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
    else:
        st.info('Processamento concluído. Selecione uma opção de saída para gerar os arquivos.')
