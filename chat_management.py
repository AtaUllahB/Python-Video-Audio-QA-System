import streamlit as st

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

def display_messages():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
