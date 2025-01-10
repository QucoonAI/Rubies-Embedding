import streamlit as st
from main import embed


st.title("RubiesAI FAQs Uploader")

def question_input():
    Question = st.text_input("Enter the Question here:")
    Answer = st.text_area("Enter the Answer here:")
    return Question, Answer

input = question_input()
if st.button('Submit FAQ'):
    if input:  # Ensure all inputs are filled
        final_output = embed(input[0], input[1])
        st.write("FAQs added successfully!")
    else:
        st.warning("Please fill out all fields before submitting.")