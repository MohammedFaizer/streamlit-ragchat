import streamlit as st
import requests

API_URL = "http://172.105.48.116:8000/api/chatbase/new-chatbot/"

def create_chatbot(name, model, system_prompt, temperature, files, urls):
    files_to_send = [("files", (file.name, file, file.type)) for file in files if file.name.endswith((".pdf", ".txt"))] if files else []
    
    data = {
        "name": name,
        "model": model,
        "system_prompt": system_prompt,
        "temperature": temperature,
        "urls": urls # Send URLs as a comma-separated string
    }
    
    response = requests.post(API_URL, data=data, files=files_to_send)
    return response.json()

st.title("BUILD CHATBOT")

name = st.text_input("Chatbot Name")
model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"])
system_prompt = st.text_area("System Prompt")
temperature = st.slider("Temperature", 0.0, 1.0, 0.3,step=0.1)

uploaded_files = st.file_uploader("Upload Files (PDF or TXT only)", accept_multiple_files=True, type=["pdf", "txt"])
# urls = st.text_area("Enter URLs (comma-separated)").split(",")
urls = [url.strip() for url in st.text_area("Enter URLs (comma-separated)").split(",") if url.strip()]


if st.button("Create Chatbot"):
    if not name:
        st.error("Chatbot name is required")
    else:
        response = create_chatbot(name, model, system_prompt, temperature, uploaded_files, urls)
        message = response.get("data", {}).get("message")
        if message:
            st.success(f"Chatbot Created! ID: {message}")
