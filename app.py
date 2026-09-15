import streamlit as st
from google import genai
import PyPDF2

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get an AI-powered ATS analysis.")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    reader = PyPDF2.PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):

        try:
            client = genai.Client(
                api_key=st.secrets["GOOGLE_API_KEY"]
            )

            prompt = f"""
You are an ATS resume analyzer.

Analyze the following resume and provide:

1. ATS Score out of 100
2. Summary
3. Strengths
4. Weaknesses
5. Missing or recommended skills
6. Specific improvement suggestions

Resume:

{resume_text}
"""

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            st.subheader("📊 Resume Analysis")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
