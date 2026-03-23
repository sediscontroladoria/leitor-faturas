import streamlit as st
import datetime
from utils.config_ui import OPCOES_MESES, OPCOES_CONTAS, OPCOES_SAIDA, OPCOES_TIPO_DEBITO

DATA_ATUAL = datetime.date.today().strftime('%Y-%m-%d')

def render_page_header(titulo: str, icon: str):
    st.title(f'{icon} {titulo}')

def select_concessionaria(key: str):
    return st.selectbox(
        'Selecione a concessionária',
        ['Sabesp', 'EDP'],
        index=0,
        key=key
    )

def select_centro_comunitario(key: str):
    return st.selectbox(
        'É centro comunitário?',
        ['Não', 'Sim'],
        index=0,
        key=key
    )

def upload_faturas_pdf(label='Arraste as faturas em PDF aqui'):
    return st.file_uploader(
        label, 
        type=['pdf'], 
        accept_multiple_files=True
    )

def select_mes_competencia(key: str):
    return st.selectbox(
        'Mês de Competência',
        OPCOES_MESES,
        index=0,
        key=key
    )

def input_ano(key: str):
    return st.text_input(
        'Ano',
        value='2026',
        key=key
    )

def select_tipo_debito(key: str):
    return st.selectbox(
        'Tipo de Débito',
        OPCOES_TIPO_DEBITO,
        index=0,
        key=key
    )

def select_conta(key: str):
    return st.selectbox(
        'Conta',
        OPCOES_CONTAS,
        index=0,
        key=key
    )

def input_complemento(key: str):
    return st.text_input(
        'Complemento',
        value='SEDIS',
        key=key
    )

class ProgressTracker:
    def __init__(self):
        self.bar = st.progress(0)
        self.text = st.empty()

    def update(self, current: int, total: int, filename: str):
        percent = (current + 1) / total
        self.bar.progress(percent)
        self.text.text(f'Processando: {filename}')

    def clear(self):
        self.bar.empty()
        self.text.empty()

def render_download_section(option: int, label: str, data: bytes, file_name: str, mime: str):
    nome_final = f'{file_name}-{DATA_ATUAL}'
    
    if option == 1:
        extensao = '.csv'
    elif option == 2:
        extensao = '.zip'
    elif option == 3:
        extensao = '.xlsx'
    else:
        extensao = ''
        
    st.download_button(
        label=label,
        data=data,
        file_name=f'{nome_final}{extensao}',
        mime=mime
    )

def select_opcoes_processamento(key: str):
    return st.multiselect(
        'O que deseja gerar?',
        OPCOES_SAIDA,
        key=key
    )