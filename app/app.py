import streamlit as st
import requests

st.title('Chatbot of sumarization')
st.header('Generate a summary of a text with .txt file')

if "resume" not in st.session_state:
    st.session_state.resume = None

upload_file = st.file_uploader("Upload a file", type=["txt"])

if upload_file is not None:
    files = {'file': (upload_file.name, upload_file.read(), upload_file.type)}

    if st.button('Summarize'):
        response = requests.post("http://127.0.0.1:8000/initialize", files=files)
        if response.status_code == 200:
            st.session_state.resume = response.json().get("summarise")
        else:
            st.write("Error")
if st.session_state.resume:
    st.write("Summarization :")
    st.write(st.session_state.resume)