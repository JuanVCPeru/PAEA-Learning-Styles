import streamlit as st
import json
import seaborn as sns
import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
from functions.utils import get_type_result_from_user

load_dotenv()

URI = os.getenv("API")
# Título do aplicativo
st.set_page_config(page_title="Título da Página", page_icon=":rocket:")
st.title("Plataforma de Avaliação de Estilos de Aprendizagem para Apoio do Professor - PAEA")
st.subheader("Questionário de Estilos de Aprendizagem de Gardner")

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

if 'form_id' not in st.session_state:
    st.session_state['form_id'] = ""

# Inserir caixa de texto para inserir o formulário
form_id_to_find = st.text_input("Digite o ID do formulário:")

# Botão para buscar o formulário na API
if st.button("Buscar Respostas"):
    # Verificar se o ID do formulário foi preenchido
    if form_id_to_find:
        # Fazer a requisição para buscar o formulário na API
        response = requests.get(f'{URI}/form_answers/{form_id_to_find}')
        
        # Verificar se a requisição foi bem sucedida
        if response.status_code == 200:
            st.success("Respostas encontradas com sucesso!")
            # Obter o formulário da resposta da API
            st.session_state['responses'] = response.json()
            st.session_state['form_id'] = form_id_to_find
            
        else:
            st.error("Falha ao buscar o formulário.")
    else:
        st.warning("Por favor, digite o ID do formulário.")

if st.session_state.responses:
    
    df = pd.DataFrame(st.session_state.responses)
    df = df.reset_index(drop=True)
    users = df['user'].unique()
    users_type_results = [
        {
            "user": user,
            "type": get_type_result_from_user(user, df)
        } for user in users
    ]
    
    users_type_table: pd.DataFrame = pd.DataFrame(users_type_results)

    # Para cada questão, mostrar os resultados da turma
    st.write("Resultados por Questão")
    for question_number in set(df['question_number'].unique()):
        question_df = df[df['question_number'] == question_number]
        question_results = question_df.groupby('answer')['user'].count().reset_index()
        question_results.columns = ['Resposta', 'Qtd de Respostas']
        question_results['Tipo'] = question_results['Resposta'].apply(lambda x: question_df[question_df['answer'] == x]['type'].iloc[0])
        st.write(f"Questão {question_number}: {question_df['question'].iloc[0]}")
        st.write(question_results)
    
    st.write("Tabela de Resultados por Usuário")
    st.write(users_type_table)

    st.write("Gráfico de Resultados por Usuário")
    # Criar um gráfico
    fig, ax = plt.subplots()
    ax.yaxis.get_major_locator().set_params(integer=True)

    sns.histplot(data=users_type_table, x='type')
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.yaxis.get_major_locator().set_params(integer=True)

    users_type_table['type'].value_counts().plot.pie(autopct='%1.1f%%')
    st.pyplot(fig)
    
    st.write('Descritivo dos dados:')
    st.write(df)