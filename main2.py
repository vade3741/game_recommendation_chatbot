import streamlit as st
st.title("Your Friendly Chatbot")
user_input = st.text_input("Which game do u want to play?")
if st.button("Submit"):
    st.write(f"Chatbot: You mentioned, '{user_input}'")
