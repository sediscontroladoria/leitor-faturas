import streamlit as st
import datetime

DATA_ATUAL = datetime.date.today().strftime('%Y-%m-%d')

def render_page_header(titulo: str, icon: str):
    st.title(f'{icon} {titulo}')

def select_concessionaria(key: str):
    return st.selectbox(
        'Selecione o tipo de fatura',
        ['Sabesp', 'EDP'],
        index=0,
        key=key
    )

def upload_faturas_pdf(label='Arraste as faturas em PDF aqui'):
    return st.file_uploader(
        label, 
        type=['pdf'], 
        accept_multiple_files=True
    )

def upload_planilha_relacao():
    return st.file_uploader(
        'Faça o upload da planilha de relação (.xlsx)', 
        type=['xlsx']
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

def render_download_section(label: str, data: bytes, file_name: str, mime: str):
    st.success('Processamento concluído com sucesso!')
    st.download_button(
        label=label,
        data=data,
        file_name=f'{file_name}-{DATA_ATUAL}.csv',
        mime=mime
    )