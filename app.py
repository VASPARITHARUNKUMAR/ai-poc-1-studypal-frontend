import streamlit as st
import requests

st.title("📚 StudyPal - Smart Assistant")

# Model selection dropdown
model_choice = st.selectbox("Choose a model:", ["groq", "ollama"])

st.subheader("Ask your question:")
query = st.text_input("Enter your question")

if st.button("Ask"):
    if query:
        try:
            with st.spinner("Thinking..."):
                res = requests.post(
                    "http://localhost:9000/chat",
                    json={"query": query, "model": model_choice},
                    timeout=15
                )
                if res.status_code == 200:
                    st.success("Answer:")
                    st.write(res.json().get("response", "No response received"))
                else:
                    st.error(f"❌ Error: {res.status_code}")
        except requests.exceptions.Timeout:
            st.error("⚠️ Request timed out.")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter a question.")
