# Import libraries
import streamlit as st         # For the web interface
import openai                  # To access OpenAI's GPT model
import os                     # To access environment variables (like your API key)

# Load your OpenAI API key (you’ll set this securely in Streamlit Cloud later)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set up the app page title and layout
st.set_page_config(page_title="Smart Note Analyzer", layout="centered")
st.title("🧠 Smart Note Analyzer")

# Let user upload a .txt or .pdf file
uploaded_file = st.file_uploader("Upload your note (txt or pdf)", type=["txt", "pdf"])

# Let user enter a question about the uploaded document
question = st.text_input("Ask a question (e.g., 'Summarize', 'What are risks?')")

# Function to extract text from uploaded file
def extract_text(file):
    if file.name.endswith(".txt"):
        # For .txt files
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        # For PDF files using PyMuPDF
        import fitz
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    return ""

# Run this block only when user clicks the button and provides input
if st.button("Analyze") and uploaded_file and question:
    with st.spinner("Analyzing..."):
        # Extract the raw text from the uploaded file
        note = extract_text(uploaded_file)

        # Create a prompt to send to the AI model
        prompt = f"Based on the following note:\n\n{note}\n\n{question}"

        # Call OpenAI's GPT-3.5 to get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4  # Lower = more focused, higher = more creative
        )

        # Show the model's answer
        st.success(response["choices"][0]["message"]["content"])
