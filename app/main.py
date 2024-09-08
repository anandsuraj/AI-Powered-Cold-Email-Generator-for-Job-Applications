import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # Set up the page configuration
    st.set_page_config(layout="wide", page_title="Cold Mail Generator for Job Applications", page_icon="📧")
    
    # Title and Description
    st.title("📧 Cold Mail Generator for Job Applications")
    st.write("This tool helps job seekers craft personalized cold emails for job applications.")
    
    # Layout with columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input Section
        st.header("Input Details")
        name_input = st.text_input("Enter your name:")
        url_input = st.text_input("Enter a URL:", value="https://sharechat.mynexthire.com/employer/jobs?src=careers&p=eyJwYWdlVHlwZSI6ImpkIiwiY3ZTb3VyY2UiOiJjYXJlZXJzIiwicmVxSWQiOjE5MTUsInJlcXVlc3RlciI6eyJpZCI6IiIsImNvZGUiOiIiLCJuYW1lIjoiIn0sInBhZ2UiOiJjYXJlZXJzIiwiYnVmaWx0ZXIiOi0xLCJjdXN0b21GaWVsZHMiOnt9fQ==")
    
    with col2:
        # Action Button
        st.header("Action")
        submit_button = st.button("Write Email")
    
    # Email Generation Section
    if submit_button:
        if not name_input:
            st.error("Please enter your name.")
        else:
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                with st.expander("Generated Emails", expanded=True):
                    for job in jobs:
                        skills = job.get('skills', [])
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links, name_input)
                        st.code(email, language='markdown')
            except Exception as e:
                st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)