import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.getenv("API")

forms = []

try:
    response = requests.get(f'{URI}/forms')
    if response.status_code == 200:
        forms = response.json()
        st.success("Forms fetched successfully!")
    else:
        st.error("Failed to fetch forms.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Display the forms in a table
st.table(forms)
