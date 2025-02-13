import streamlit as st 
import requests
import json

from langchain_openai import ChatOpenAI

if "rows" not in st.session_state:
    st.session_state.rows = []

st.title("RAG ACTIONS")
st.text("Rules:")
st.caption("1.Never give the Action name twice.")
st.caption("2.Action name-(use '_' for spacing)")
st.caption("3.Add variables which need to be called by your api")
st.caption("4.use double curly brackets wherever you want the variables to be used")
st.caption("5.If you add a variable  (var_name)'character_name' | (var_type) 'string'| (var_desc) 'you should fetch character name ")
st.caption("  Ex: url=https://api.disneyapi.dev/character ")
st.caption("6. query params key:name   value:{{character_name}}")
st.caption("7.naming should be clear,so ai can figure when to use")
st.markdown('---')

chatbot_id = st.text_input("Enter the chatbot id")
action_name = st.text_input("Enter the action Name ")
action_desc = st.text_area("When To Use")

def add_row():
    st.session_state.rows.append({"name": "", "type": "string", "description": ""})

def remove_row(index):
    st.session_state.rows.pop(index)
    st.rerun()

st.button("➕ variable", on_click=add_row)

type_options = ["string", "number"]

for i, row in enumerate(st.session_state.rows):
    col1, col2, col3, col4 = st.columns([3, 3, 4, 1])
    
    with col1:
        st.session_state.rows[i]["name"] = st.text_input(f"Name {i+1}", row["name"], key=f"name_{i}")
    
    with col2:
        st.session_state.rows[i]["type"] = st.selectbox(f"Type {i+1}", type_options, 
                                                          index=type_options.index(row["type"]) if row["type"] in type_options else 0, 
                                                          key=f"type_{i}")
    
    with col3:
        st.session_state.rows[i]["description"] = st.text_input(f"Description {i+1}", row["description"], key=f"description_{i}")
    
    with col4:
        if st.button("❌", key=f"remove_{i}"):
            remove_row(i)

def add_fields(field_type):
    """Dynamically add key-value fields for Params, Headers, or Body"""
    fields = {}
    with st.expander(f"{field_type}", expanded=False):
        count = st.number_input(f"Number of {field_type}", min_value=0, step=1, key=f"{field_type}_count")
        for i in range(count):
            col1, col2 = st.columns(2)
            key = col1.text_input(f"{field_type} Key {i+1}", key=f"{field_type}_key_{i}")
            value = col2.text_input(f"{field_type} Value {i+1}", key=f"{field_type}_value_{i}")
            if key:
                fields[key] = value
    return fields

method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"])
url = st.text_input("Enter URL")

params = add_fields("Query Parameters")
headers = add_fields("Headers")
body = add_fields("JSON Body") if method in ["POST", "PUT"] else {}

backend_url = "http://172.105.48.116:8000/api/chatbase/add-tool/"

data_payload = {
    "chatbot_id": chatbot_id,
    "action_name": action_name,
    "action_desc": action_desc,
    "variables": st.session_state.rows,
    "method": method,
    "url": url,
    "params": params,
    "headers": headers,
    "body": body,
}

if st.button("Send Data"):
    response = requests.post(backend_url, json=data_payload)
    
    if response.status_code == 200:
        st.success("Data sent successfully!")
        st.json(response.json())
    else:
        st.error(f"Failed to send data: {response.status_code}")
        st.text(response.text)
