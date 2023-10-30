import streamlit as st
import requests
import pandas as pd
from pyresparser import ResumeParser

st.set_page_config(
    page_title="LinkedIn Profile and Resume Analyzer",
    page_icon=":mag:",
)

st.title("LinkedIn Profile and Resume Analyzer")

# LinkedIn Profile Data Extraction Section
st.header("LinkedIn Profile Data Extraction")

# Input field for LinkedIn profile URL
linkedin_profile_url = st.text_input("Enter a LinkedIn Profile URL")

# API endpoint and API key for LinkedIn Profile Data Extraction
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
api_key = '3dk-Ilfzlsl6VctMJIQ-Iw'  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}

# Skill extraction checkbox
extract_skills = st.checkbox("Extract Skills")

if st.button("Extract Profile Data"):
    if linkedin_profile_url:
        with st.spinner("Extracting profile data..."):
            params = {'url': linkedin_profile_url}
            if extract_skills:
                params['skills'] = 'include'

            response = requests.get(api_endpoint, params=params, headers=headers)
            if response.status_code == 200:
                profile_data = response.json()

                if 'full_name' in profile_data:
                    full_name = profile_data['full_name']
                    st.subheader("LinkedIn Profile Full Name")
                    st.write(full_name)
                else:
                    st.warning("No full name found in the LinkedIn profile data.")

                if 'skills' in profile_data:
                    skills = profile_data['skills']
                    st.subheader("LinkedIn Profile Skills")
                    for skill in skills:
                        st.write(f"- {skill}")
                else:
                    st.warning("No skills found in the LinkedIn profile data.")
            else:
                st.error(f"Error: Unable to fetch LinkedIn profile data. Status code: {response.status_code}")
    else:
        st.warning("Please enter a valid LinkedIn profile URL.")

# Resume Analysis Section
st.header("Resume Analysis")

# Resume upload section
st.subheader("Upload your resume (PDF)")
pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])

if pdf_file is not None:
    save_image_path = './Uploaded_Resumes/' + pdf_file.name
    with open(save_image_path, "wb") as f:
        f.write(pdf_file.getbuffer())
    st.write("Resume uploaded successfully!")

# Resume analysis checkbox
analyze_resume = st.checkbox("Analyze Resume")

if analyze_resume:
    if pdf_file:
        st.subheader("Resume Content:")
        pdf_content = b""
        with open(save_image_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()
            st.text(pdf_content)  # Removed the .decode("utf-8") part

        st.subheader("Resume Analysis Results:")
        resume_data = ResumeParser(save_image_path).get_extracted_data()
        if resume_data:
            st.success("Resume analysis complete.")
            st.json(resume_data)
        else:
            st.error("Failed to analyze the resume. Please upload a valid PDF resume.")

# Additional options
st.header("Additional Options")
extracted_skills = []

if extract_skills and "skills" in profile_data:
    extracted_skills = profile_data["skills"]

st.subheader("Extracted Skills:")
st.write(extracted_skills)

# You can add more features here as needed

