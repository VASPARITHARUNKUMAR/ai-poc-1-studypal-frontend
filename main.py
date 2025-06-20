# main.py

import streamlit as st
from api_client import upload_documents, ask_question

st.set_page_config(page_title="StudyPal", layout="centered")
st.title("📘 StudyPal – AI-Powered Study Assistant")

st.markdown("Upload your semester/subject documents and ask questions directly from them.")

# --- Upload Section ---
st.header("📄 Upload Documents")

semester = st.text_input("Semester (e.g., Fall 2024)")
subject = st.text_input("Subject (e.g., Data Structures)")
files = st.file_uploader("Upload PDF, DOCX, or TXT files", accept_multiple_files=True, type=['pdf', 'docx', 'txt'])

if st.button("Upload"):
    if not semester or not subject or not files:
        st.warning("Please provide all inputs before uploading.")
    else:
        with st.spinner("Uploading and processing..."):
            result = upload_documents(files, semester, subject)
            if result.get("status") == "error":
                st.error(result.get("message"))
            else:
                st.success("Documents uploaded and indexed successfully!")

# --- Chat Section ---
st.header("💬 Ask a Question")

question = st.text_input("Your question")
model = st.selectbox("Choose Model", ["groq", "ollama", "openai"])

if st.button("Ask"):
    if not question or not semester or not subject:
        st.warning("Please provide all required inputs before asking.")
    else:
        with st.spinner("Thinking..."):
            response = ask_question(question, semester, subject, model)
            if response.get("status") == "error":
                st.error(response.get("message"))
            else:
                st.write("**Answer:**", response)

