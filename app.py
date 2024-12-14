import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to fetch Gemini response
def get_gemini_response(resume_text, job_description):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{resume_text}
description:{job_description}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Enhanced Profile Summary":"", "Key Improvements":"", "Final Suggestions":""}}
"""


    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Streamlit UI
st.set_page_config(page_title="HireFit - Your Job Match Optimizer", page_icon="💼", layout="wide")

# Header section
st.title("🔧 HireFit")
st.markdown("Improve Your Resume's ATS Compatibility")

# Sidebar for instructions
with st.sidebar:
    st.header("Instructions")
    st.write("1. Paste the job description in the text area provided.")
    st.write("2. Upload your resume in PDF format.")
    st.write("3. Click the **Submit** button to analyze your resume.")
    st.write("4. Review the detailed feedback for improvements.")
    st.info("Ensure the resume is updated and formatted as a PDF.")

# Input sections
st.subheader("Job Description")
job_description = st.text_area("Paste the Job Description", height=150, placeholder="Enter the job description here...")

st.subheader("Upload Resume")
uploaded_file = st.file_uploader("Upload Your Resume (PDF format only)", type="pdf")

# Submit button
if st.button("🔄 Analyze Resume"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing your resume... This might take a few seconds."):
            # Extract text from uploaded file
            resume_text = input_pdf_text(uploaded_file)
            # Get Gemini response
            try:
                response = get_gemini_response(resume_text, job_description)
                st.success("Analysis Complete!")
                st.subheader("Results")
                st.json(response)
            except Exception as e:
                st.error("An error occurred while processing your request.")
                st.write(e)
    else:
        st.warning("Please upload your resume and enter a job description to proceed.")

# Footer section
st.markdown("---")
st.markdown(
    "Developed with ❤️ by HireFit :) | Powered by Google Gemini AI"
)
