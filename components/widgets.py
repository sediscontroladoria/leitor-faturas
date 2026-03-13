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

def render_download_section(option:int, label: str, data: bytes, file_name: str, mime: str):
    file_name = f'{file_name}-{DATA_ATUAL}'
    st.download_button(
        label=label,
        data=data,
        file_name=f'{file_name}.csv' if option==1 else  f'{file_name}.zip',
        mime=mime
    )