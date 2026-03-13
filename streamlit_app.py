import streamlit as st

st.set_page_config(page_title='Processamento de Faturas', layout='wide')

pg = st.navigation({
    'Principal': [
        st.Page('pages/00_home.py', title='Home', icon='🏠')
    ],
    'Ferramentas': [
        st.Page('pages/01_leitor_faturas.py', title='Leitor de Faturas', icon='📄', default=True),
    ]
})

pg.run()