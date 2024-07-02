import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv("API")

forms = []

st.subheader('Formulários disponíveis')

try:
    response = requests.get(f'{URI}/forms')
    if response.status_code == 200:
        forms = response.json()
    else:
        st.error("Failed to fetch forms.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Display the forms in a table
st.write('Lista de formulários:')
st.table(forms)
