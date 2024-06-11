import streamlit as st
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o JSON
# Carregar o JSON
with open('data/questions/dog_cat.json', encoding='utf-8') as f:
    data = json.load(f)

# Título do aplicativo
st.title("Plataforma de Avaliação de Estilos de Aprendizagem para Apoio do Professor - PAEA")

# Dicionário para armazenar as respostas do usuário
responses = {type_: 0 for type_ in data['types']}

# Criar o formulário dinamicamente
st.header("Por favor, responda as seguintes questões:")
for question in data['questions']:
    st.write(question['question'])
    options = {answer['answer']: (answer['type'], answer['points']) for answer in question['answers']}
    selected_answer = st.radio("", list(options.keys()), key=question['question'])
    responses[options[selected_answer][0]] += options[selected_answer][1]

# Botão de submissão
if st.button("Submeter"):
    # Preparar os dados para o gráfico de pizza
    labels = responses.keys()
    sizes = responses.values()
    
    # Configurar o estilo do Seaborn
    sns.set_theme(style="whitegrid")
    
    # Plotar gráfico de pizza usando Matplotlib (Seaborn não tem uma função para gráficos de pizza)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)