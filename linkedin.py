import streamlit as st
import requests

st.title("LinkedIn Profile Data Extractor")

# Input field for LinkedIn profile URL
linkedin_profile_url = st.text_input("Enter a LinkedIn Profile URL")

# API endpoint and API key
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
api_key = '3dk-Ilfzlsl6VctMJIQ-Iw'  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}

if st.button("Extract Profile Data"):
    if linkedin_profile_url:
        with st.spinner("Extracting profile data..."):
            response = requests.get(api_endpoint, params={'url': linkedin_profile_url, 'full_name': 'include', 'skills': 'include'}, headers=headers)
            if response.status_code == 200:
                profile_data = response.json()

                # Check if 'full_name' and 'skills' are present in the response
                if 'full_name' in profile_data:
                    full_name = profile_data['full_name']
                    st.subheader("Full Name")
                    st.write(full_name)
                else:
                    st.warning("No full name found in the LinkedIn profile data.")

                if 'skills' in profile_data:
                    skills = profile_data['skills']
                    st.subheader("Skills")
                    for skill in skills:
                        st.write(f"- {skill}")
                else:
                    st.warning("No skills found in the LinkedIn profile data.")
            else:
                st.error(f"Error: Unable to fetch LinkedIn profile data. Status code: {response.status_code}")
    else:
        st.warning("Please enter a valid LinkedIn profile URL.")

