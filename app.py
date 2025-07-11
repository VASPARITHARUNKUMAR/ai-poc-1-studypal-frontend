import streamlit as st
import requests

BACKEND = "http://localhost:9000"

st.title("📚 StudyPal - Smart Assistant")

menu = ["Chat with Assistant", "Upload Documents"]
choice = st.sidebar.selectbox("Select Option", menu)

if choice == "Chat with Assistant":
    model = st.selectbox("Choose a model:", ["groq", "ollama"])
    query = st.text_input("Ask your question:")

    if st.button("Ask"):
        if not query:
            st.warning("Please enter a question")
        else:
            with st.spinner("Thinking..."):
                res = requests.post(f"{BACKEND}/chat", json={"query": query, "model": model})
                if res.status_code == 200:
                    st.markdown("**Answer:**\n" + res.json().get("response", "No response"))
                else:
                    st.error("Error: " + res.text)

elif choice == "Upload Documents":
    st.subheader("Upload Documents")
    semester = st.text_input("Semester")
    subject = st.text_input("Subject")
    uploaded_file = st.file_uploader("Upload your study material (PDF, DOC, DOCX, PPTX, XLSX, CSV, MD, TXT, JPG, PNG)", type=["pdf", "doc", "docx", "pptx", "xlsx", "csv", "md", "txt", "jpg", "jpeg", "png"]
)
    if st.button("Upload"):
        if uploaded_file and semester and subject:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"semester": semester, "subject": subject}
            try:
                res = requests.post(f"{BACKEND}/upload", files=files, data=data)
                if res.status_code == 200:
                    st.success(res.json().get("status", "Upload successful"))
                else:
                    st.error(f"Upload failed with status {res.status_code}")
            except Exception as e:
                st.error(f"Error during upload: {e}")
        else:
            st.warning("Please fill all fields and upload a file")