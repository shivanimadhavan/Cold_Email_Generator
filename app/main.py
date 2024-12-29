import streamlit as st
import os
os.environ['USER_AGENT'] = "ColdMailGenerator/1.0 (compatible; Python/3.9)"
from langchain_community.document_loaders import WebBaseLoader
from chain import Chain
from portfolio import Portfolio 
from utils import clean_text
import requests

class main:
    
 def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="")
    submit_button = st.button("Submit")
    
    if submit_button:
       try:
            loader = WebBaseLoader([url_input])        
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
       except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__=='__main__':
    chain=Chain()
    portfolio=Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    main.create_streamlit_app(chain, portfolio, clean_text)