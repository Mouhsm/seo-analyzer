import streamlit as st
import requests
import os

# Get the API key from the environment variable
API_KEY = os.getenv('API_KEY')

# Set up the Streamlit app
st.title('Website SEO Analyzer')
st.write('Enter a URL below to generate an SEO report.')

# Input field for URL
url = st.text_input('Enter URL:')

# Function to fetch SEO report
def get_seo_report(url):
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'website-seo-analyzer1.p.rapidapi.com'
    }
    querystring = {'url': url}
    url = 'https://website-seo-analyzer1.p.rapidapi.com/api'

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f'Error fetching SEO report: {response.status_code} - {response.text}')

# Generate SEO report button
if st.button('Get SEO Report'):
    if url:
        with st.spinner('Generating SEO report...'):
            seo_data = get_seo_report(url)

            if seo_data:
                st.subheader('SEO Report:')
                st.json(seo_data)  # Displaying the JSON response
            else:
                st.error('Failed to fetch SEO report. Please check the URL and try again.')
    else:
        st.warning('Please enter a URL to generate the SEO report.')
