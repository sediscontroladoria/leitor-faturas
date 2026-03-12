import streamlit as st

def home():
    st.title('Sistema de Processamento de Faturas')
    st.markdown('''
    ## Prefeitura Municipal de Taubaté
    Esta ferramenta foi desenvolvida para automatizar a leitura e organização de faturas.
    Utilize o menu lateral para acessar as funcionalidades.
    ''')
    
if __name__ == '__main__':
    home()