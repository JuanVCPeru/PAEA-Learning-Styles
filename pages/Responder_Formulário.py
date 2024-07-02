import streamlit as st
import json
import seaborn as sns
import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import time
import pandas as pd
# Carregar o JSON

load_dotenv()

URI = os.getenv("API")
# Título do aplicativo
st.set_page_config(page_title="Título da Página", page_icon=":rocket:")
st.title("Plataforma de Avaliação de Estilos de Aprendizagem para Apoio do Professor - PAEA")
st.subheader("Questionário de Estilos de Aprendizagem")

if 'form_name' not in st.session_state:
    st.session_state['form_name'] = ""

if 'form_id' not in st.session_state:
    st.session_state['form_id'] = ""

if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# Inserir caixa de texto para inserir o formulário
form_id_to_find = st.text_input("Digite o ID do formulário:")


# Botão para buscar o formulário na API
if st.button("Buscar formulário"):
    # Verificar se o ID do formulário foi preenchido
    if form_id_to_find:
        # Fazer a requisição para buscar o formulário na API
        response = requests.get(f'{URI}/form/{form_id_to_find}')
        
        # Verificar se a requisição foi bem sucedida
        if response.status_code == 200:
            st.success("Formulário encontrado com sucesso!")
            # Obter o formulário da resposta da API
            form = response.json()
            st.session_state.form_name = form['name']
            st.session_state.form_id = form_id_to_find
            
        else:
            st.error("Falha ao buscar o formulário.")
    else:
        st.warning("Por favor, digite o ID do formulário.")


if st.session_state.form_name:
    with open(f'data/questions/{st.session_state.form_name}.json', encoding='utf-8') as f:
        data = json.load(f)

    # Dicionário para armazenar as respostas do usuário
    responses = {}

    # Criar o formulário dinamicamente
    st.header("Por favor, responda as seguintes questões:")

    # Inserir caixa de texto para inserir o nome
    name = st.text_input("Digite seu nome:")

    for index, question in enumerate(data['questions'], 1):
        st.write(question['question'])
        options = {answer['answer']: (answer['type'], answer['points']) for answer in question['answers']}
        selected_answer = st.radio("", list(options.keys()), key=question['question'])
        # responses[options[selected_answer][0]] += options[selected_answer][1]
        
        # Save the question, selected answer, and points in the responses dictionary
        responses[index] = {
            'question': question['question'],
            'answer': selected_answer,
            'type': options[selected_answer][0],
            'points': options[selected_answer][1]
        }

    # Save the responses in session_state
    st.session_state['responses'] = responses

    # Botão de submissão
    if st.button("Submeter"):

        # Check if all fields are filled
        if not name or len(name) < 2:
            st.warning("Por favor, digite seu nome.")
        else:
            # Create a dictionary to store the user's answers
            user_answers = []

            # Iterate over the questions
            final_response: dict[int, dict] = st.session_state['responses']
            for question_number, answer in final_response.items():
                
                # Get the question text
                f_question = answer['question']
                f_answer = answer['answer']
                f_type = answer['type']
                f_points = answer['points']

                answer_dict = {
                    'question': f_question,
                    'answer': f_answer,
                    'type': f_type,
                    'points': f_points,
                    'question_number': question_number,
                    'user': name,
                    'form_id': st.session_state.form_id,
                }
                                
                user_answers.append(answer_dict)
            
            # # Show a spinner while sending the answers to the API
            # with st.spinner('Submitting answers...'):
            #     # Send each user answer to the API
            #     for answer in user_answers:

            #         response = requests.post(f'{URI}/answer', json=answer)
            #         if response.status_code == 200:
            #             st.success("Resposta enviada com sucesso!")
            #         else:
            #             st.error("Falha ao enviar a resposta.")
                    
            #         time.sleep(0.5)
            
            # # Hide the spinner once the answers are submitted
            # st.spinner(None)

            # Calculate the total points for each type
            type_points = {type_: 0 for type_ in data['types']}
            for answer in user_answers:
                type_points[answer['type']] += answer['points']

            # Find the type with the highest points
            max_points = max(type_points.values())
            max_type = [type_ for type_, points in type_points.items() if points == max_points]

            # Display the type with the highest points
            st.write(f"O seu estilo de aprendizagem predominante é: {max_type[0]}")

            # Gráfico de pontos por tipo
            answers_df = pd.DataFrame(user_answers)
            fig, ax = plt.subplots()
            # rotate the x labels in 90 degrees
            plt.xticks(rotation=90)
            sns.barplot(data=answers_df.groupby('type')['points'].sum().reset_index(), x='type', y='points', ax=ax)
            st.pyplot(fig)