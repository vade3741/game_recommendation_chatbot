import streamlit as st
import requests
st.title("Your Friendly Chatbot")

user_input = st.text_input("Which game do you want to play?")
if st.button("Submit"):
    if user_input:
        url = "http://127.0.0.1:8000/qa"
        payload = {"query": user_input}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            st.write(f"Chatbot: {response_data['response']}")
        else:
            st.write(f"Chatbot: Sorry, something went wrong. (Error {response.status_code})")
    else:
        st.write("Please enter a game name.") 
