import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import streamlit as st
from streamlit import spinner
from urllib.parse import urlparse
import time

nltk.download('stopwords')
nltk.download('punkt_tab')

st.title('SEO Analyzer')
st.write('Get a comprehensive SEO analysis to optimize your website’s visibility')

# Custom CSS for button styling
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #1f3a93;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.4s;
    }
    .stButton > button:hover {
        background-color: #3c6382;
        color: white;
    }
    .stButton > button:active {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

url = st.text_input('URL:', placeholder='Enter URL here')

def seo_analysis(url):
    good = []
    bad = []

    response = requests.get(url)
    if response.status_code != 200:
        st.error("Error: Unable to access the website.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Measure page load time
    start_time = time.time()
    requests.get(url)
    load_time = time.time() - start_time
    if load_time < 3:
        good.append(f"Page Load Time: {load_time:.2f} seconds (Fast)")
    else:
        bad.append(f"Page Load Time: {load_time:.2f} seconds (Slow)")

    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    if title and title.get_text():
        good.append("Title Exists! Great!")
    else:
        bad.append("Title does not exist! Add a Title")

    if description and description.get('content'):
        good.append("Description Exists! Great!")
    else:
        bad.append("Description does not exist! Add a Meta Description")

    hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    h_tags = []
    for h in soup.find_all(hs):
        good.append(f"{h.name} --> {h.text.strip()}")
        h_tags.append(h.name)

    if 'h1' not in h_tags:
        bad.append("No H1 found!")

    for i in soup.find_all('img', alt=''):
        bad.append(f"No Alt: {i}") 

    bod = soup.find('body').text
    words = [i.lower() for i in word_tokenize(bod)]
    bi_grams = ngrams(words, 2)
    freq_bigrams = nltk.FreqDist(bi_grams)
    bi_grams_freq = freq_bigrams.most_common(10)

    sw = nltk.corpus.stopwords.words('english')
    new_words = [i for i in words if i not in sw and i.isalpha()]

    freq = nltk.FreqDist(new_words)
    keywords = freq.most_common(10)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Keywords', 'Bigrams', 'Good', 'Bad', 'Links', 'Performance'])
    with tab1:
        st.subheader('Top Keywords')
        for i in keywords:
            st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>{i[0]}: {i[1]}</div>", unsafe_allow_html=True)
    with tab2:
        st.subheader('Top Bigrams')
        for i in bi_grams_freq:
            st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>{i[0]}: {i[1]}</div>", unsafe_allow_html=True)
    with tab3:
        st.subheader('Good Points')
        for i in good:
            st.success(i)
    with tab4:
        st.subheader('Warnings')
        for i in bad:
            st.error(i)
    with tab5:
        st.subheader('Links')
        internal_links = [a['href'] for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc == urlparse(url).netloc]
        external_links = [a['href'] for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc != urlparse(url).netloc]
        st.markdown(f"Internal Links: {len(internal_links)}")
        st.markdown(f"External Links: {len(external_links)}")
        st.markdown("Broken Links:")
        for link in internal_links + external_links:
            try:
                r = requests.get(link)
                if r.status_code != 200:
                    st.markdown(f"<div style='background-color: #ffcccc; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>{link}</div>", unsafe_allow_html=True)
            except:
                st.markdown(f"<div style='background-color: #ffcccc; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>{link}</div>", unsafe_allow_html=True)
    with tab6:
        st.subheader('Performance')
        st.markdown(f"Page Load Time: {load_time:.2f} seconds")
        st.markdown(f"Mobile-Friendliness: {'Yes' if 'viewport' in [meta.get('name') for meta in soup.find_all('meta')] else 'No'}")

if st.button('Start Analysis') or (url and st.session_state.get('url', '') != url):
    if not is_valid_url(url):
        st.error("Please enter a valid URL.")
    else:
        with spinner('Getting SEO details...'):
            seo_analysis(url)
        st.session_state['url'] = url

if url and st.session_state.get('url', '') != url:
    if not is_valid_url(url):
        st.error("Please enter a valid URL.")
    else:
        seo_analysis(url)
        st.session_state['url'] = url
