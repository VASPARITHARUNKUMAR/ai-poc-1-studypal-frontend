import streamlit as st
import requests

st.title("📚 StudyPal - Smart Study Assistant")

menu = ["Upload Material", "Chat with Assistant"]
choice = st.sidebar.selectbox("Select Option", menu)

if choice == "Upload Material":
    st.subheader("Upload Documents")
    semester = st.text_input("Semester")
    subject = st.text_input("Subject")
    uploaded_file = st.file_uploader("Upload your study material (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if st.button("Upload"):
        if uploaded_file and semester and subject:
            res = requests.post(
                "http://localhost:8000/upload",
                files={"file": uploaded_file.getvalue()},
                data={"semester": semester, "subject": subject},
            )
            st.success(res.json()["status"])

elif choice == "Chat with Assistant":
    st.subheader("Ask Questions from Your Documents")
    user_query = st.text_input("Enter your question")
    if st.button("Ask"):
        if user_query:
            res = requests.post("http://localhost:8000/chat", json={"query": user_query})
            st.write("**Answer:**", res.json()["response"])