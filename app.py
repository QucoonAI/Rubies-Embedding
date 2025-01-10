import streamlit as st
from main import update_faq, embed_query, query_top_k


st.title("RubiesAI FAQs Uploader")

def question_input():
    Question = st.text_input("Enter the Question here:")
    Answer = st.text_area("Enter the Answer here:")
    return Question, Answer

input = question_input()
if st.button('Submit FAQ'):
    if input:  # Ensure all inputs are filled
        final_output = update_faq(input[0], input[1])
        st.write("FAQs added successfully!")
    else:
        st.warning("Please fill out all fields before submitting.")



# Initialize session state for buttons
if 'show_update_form' not in st.session_state:
    st.session_state.show_update_form = False
if 'submit_updates' not in st.session_state:
    st.session_state.submit_updates = False
if 'faqs' not in st.session_state:
    st.session_state['faqs'] = []

# Function to display editable FAQs
def display_editable_faqs(faqs):
    edited_faqs = []
    for faq in faqs:
        st.write(f"**FAQ ID: {faq['id']}**")
        question = st.text_input(f"Edit Question (ID: {faq['id']})", value=faq['question'], key=f"question_{faq['id']}")
        answer = st.text_area(f"Edit Answer (ID: {faq['id']})", value=faq['answer'], key=f"answer_{faq['id']}")
        edited_faqs.append({"id": faq['id'], "question": question, "answer": answer})
        st.write("---")
    return edited_faqs


# Button to display editable FAQs
if st.button("Update FAQ"):
    st.session_state.show_update_form = True

# Display the query input and button if the form should be shown
if st.session_state.show_update_form:
    query = st.text_input("What Question are you trying to update?")
    if st.button("Query DB"):
        if query:
            query_vector = embed_query(query)
            if query_vector:
                faqs = query_top_k(query_vector, top_k=3)
                # Convert list of tuples to list of dictionaries
                st.session_state.faqs = [{'id': id_, 'question': question, 'answer': answer} for id_, question, answer in faqs]
            else:
                st.warning("Failed to generate query vector.")
        else:
            st.warning("Please enter a question to query.")

# Display the editable FAQs if they exist in session state
if st.session_state.faqs:
    for faq in st.session_state.faqs:
        st.text_input(f"Edit Question (ID: {faq['id']})", value=faq['question'], key=f"question_{faq['id']}")
        st.text_area(f"Edit Answer (ID: {faq['id']})", value=faq['answer'], key=f"answer_{faq['id']}")
        st.write("---")

    if st.button("Submit Updates"):
        # Process the updates
        updated_faqs = []
        for faq in st.session_state.faqs:
            updated_question = st.session_state.get(f"question_{faq['id']}", faq['question'])
            updated_answer = st.session_state.get(f"answer_{faq['id']}", faq['answer'])
            if updated_question != faq['question'] or updated_answer != faq['answer']:
                updated_faqs.append({
                    'id': faq['id'],
                    'question': updated_question,
                    'answer': updated_answer
                })
        if updated_faqs:
            st.write("The following FAQs have been updated:")
            for faq in updated_faqs:
                update_faq(faq['question'], faq['answer'], faq['id'])
                st.write(f"**ID:** {faq['id']}")
                st.write(f"**Question:** {faq['question']}")
                st.write(f"**Answer:** {faq['answer']}")
                st.write("---")
            # Here you can add the logic to update the database with the updated_faqs
        else:
            st.write("No changes detected.")
