import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("API")

# Título do aplicativo
st.set_page_config(page_title="Crear Formulário", page_icon=":rocket:")
st.title("Crear un Formulário")
form_text = ""
form_id = ""

# Criar um select para escolher uma das opções de arquivo dentro de data/questions
file_options = [file.replace('.json', '') for file in os.listdir('data/questions')]
selected_file = st.selectbox('Selecione um arquivo:', file_options)

# Botão para confirmar o formulário
if st.button('Confirmar'):
    form_json = {
        "name": selected_file,
    }
    response = requests.post(f'{URI}/form', json=form_json)
    if response.status_code == 200:
        st.success("Answer submitted successfully!")
        form_json = response.json()
        form_id = form_json['form_id']
        form_text = f'Formulário criado com sucesso! ID: {form_id}'
    else:
        st.error("Failed to submit answer.")
    
if form_id:
    st.text(form_text)
