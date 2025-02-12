import streamlit as st
import requests

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = None


if "chatbot_name" not in st.session_state:    
    st.session_state["chatbot_name"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []


# API Endpoints
list_chatbots_url = "http://172.105.48.116:8000/api/chatbase/list-chatbot/"
new_thread_url = "http://172.105.48.116:8000/api/chatbase/new-thread/"


if 'thread_id' in st.session_state and st.session_state.thread_id:
    st.subheader(f"Chat with {st.session_state.chatbot_name}")

    # Get user input
    user_question = st.chat_input("Please enter your question")

    for msg in st.session_state.messages:
        with st.chat_message("user"):
            st.write(msg["user"])
        with st.chat_message("assistant"):
            st.write(msg["assistant"])

    if user_question:
        # Display user message
        with st.chat_message("user"):
            st.write(user_question)

        # Prepare the payload for the API
        payload = {
            "thread_id": st.session_state.thread_id,
            "user_question": user_question
        }
        
        # Send the request to the chatbase API
        response = requests.post("http://172.105.48.116:8000/api/chatbase/chat/", json=payload)

        # If the response is successful, display the assistant's response
        if response.status_code == 200:
            assistant_answer = response.json().get("data", {}).get("answer", "")
            st.session_state.messages.append({"user": user_question, "assistant": assistant_answer})
            # Display assistant response
            with st.chat_message("assistant"):
                st.write(assistant_answer)
            
        else:
            st.write("Error: Unable to get a response from the assistant.")






else:

    # Fetch available chatbots
    response = requests.get(list_chatbots_url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        chatbot_options = {f"{chatbot['name']} (ID: {chatbot['id']})": chatbot["id"] for chatbot in data}
        selected_chatbot = st.selectbox("Choose Your Chatbot", list(chatbot_options.keys()))
    else:
        st.error("Failed to fetch chatbots")
        chatbot_options = {}
        selected_chatbot = None

    # Start Chat button
    if st.button("Start Chat"):
        if selected_chatbot:
            chatbot_id = chatbot_options[selected_chatbot]
            payload = {"chatbot_id": chatbot_id}
            thread_response = requests.post(new_thread_url, json=payload)

            if thread_response.status_code == 200:
                thread_data = thread_response.json().get("data", {})
                thread_id = thread_data.get("thread_id")
                chatbot_name = thread_data.get("chatbot_name")

                # Store thread details in session state
                st.session_state.thread_id = thread_id
                st.session_state.chatbot_name = chatbot_name
                st.session_state.messages = [] 
                st.rerun()
            else:
                st.error("Failed to start a new chat thread")



# Chat Interface
