import streamlit as st
import requests

# Backend URL
BACKEND = "http://localhost:8000"

# Page Configuration
st.set_page_config(page_title="StudyPal - Smart Assistant", page_icon="📚", layout="wide")
st.title("📚 StudyPal - Smart Assistant")
st.markdown("Your personal academic companion 🤖")

# Sidebar Menu
menu = ["💬 Chat with Assistant", "📤 Upload Documents"]
choice = st.sidebar.selectbox("Select an option", menu)

# Chat Section
if choice == "💬 Chat with Assistant":
    st.subheader("💡 Chat with StudyPal")
    st.markdown("Ask any academic-related question below 👇")

    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("💬 Your Question:")
    with col2:
        model = st.selectbox("🤖 Select Model:", ["groq", "ollama"])

    ask_button = st.button("🚀 Ask Assistant")

    if ask_button:
        if not query.strip():
            st.warning("⚠️ Please enter a question before submitting.")
        else:
            with st.spinner("🤔 Thinking..."):
                try:
                    response = requests.post(f"{BACKEND}/chat", json={"query": query, "model": model})
                    if response.status_code == 200:
                        answer = response.json().get("response", "No response received.")
                        st.success("✅ Answer received!")
                        st.markdown(f"**🧠 StudyPal:** {answer}")
                    else:
                        st.error(f"❌ Failed to get a response. Server says: {response.text}")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")

# Upload Section
elif choice == "📤 Upload Documents":
    st.subheader("📄 Upload Your Study Materials")
    st.markdown("Help StudyPal learn by uploading your academic content ✍️")

    semester = st.text_input("📆 Semester:")
    subject = st.text_input("📘 Subject:")
    uploaded_file = st.file_uploader("📎 Upload File", type=["pdf", "doc", "docx", "pptx", "xlsx", "csv", "md", "txt", "jpg", "jpeg", "png"])

    if st.button("📤 Upload"):
        if semester and subject and uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"semester": semester, "subject": subject}

            with st.spinner("📡 Uploading file..."):
                try:
                    response = requests.post(f"{BACKEND}/upload", files=files, data=data)
                    if response.status_code == 200:
                        st.success("✅ Upload successful!")
                        st.markdown(f"**File Name:** `{uploaded_file.name}`")
                        st.markdown(f"**Subject:** `{subject}` | **Semester:** `{semester}`")
                    else:
                        st.error(f"❌ Upload failed. Status: {response.status_code}")
                except Exception as e:
                    st.error(f"⚠️ Error during upload: {e}")
        else:
            st.warning("⚠️ Please fill in all fields and upload a file.")
