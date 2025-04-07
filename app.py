import streamlit as st
import openai
import os

# -----------------------------
# 🔐 Password protection
# -----------------------------
PASSWORD = "letmein123"  # ✅ Change this to your own password
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Protected App")
    pwd = st.text_input("Enter password to access:", type="password")
    if pwd == PASSWORD:
        st.session_state.authenticated = True
        st.success("Access granted!")
        st.experimental_rerun()
    else:
        if pwd:
            st.error("Incorrect password. Please try again.")
    st.stop()

# -----------------------------
# 🧠 Smart Note Analyzer Starts Here
# -----------------------------

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Smart Note Analyzer", layout="centered")
st.title("🧠 Smart Note Analyzer")

uploaded_file = st.file_uploader("Upload your note (txt or pdf)", type=["txt", "pdf"])
question = st.text_input("Ask a question (e.g., 'Summarize', 'What are risks?')")

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        import fitz
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    return ""

if st.button("Analyze") and uploaded_file and question:
    with st.spinner("Analyzing..."):
        note = extract_text(uploaded_file)
        prompt = f"Based on the following note:\n\n{note}\n\n{question}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        st.success(response["choices"][0]["message"]["content"])
