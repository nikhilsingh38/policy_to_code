# main.py
import streamlit as st
import PyPDF2
from ptc_langchain_helper import extract_text_from_pdf,extract_specific_topics,generate_rego_and_firewall_rules

st.set_page_config(page_title="Policy to Code", page_icon="📈", layout="wide")

st.markdown("""
<nav class="custom-navbar">
    <a href="#">
        <img src="http://upscalenet.com/wp-content/uploads/2024/02/pwcLogo.png" class="imgCon" alt="Logo" >
    </a>    
    <div class="navContainer">
        <button class="btn">About Product</button>
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
            <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
            <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
        </svg>
    </div>
</nav>
""", unsafe_allow_html=True)

with open('../ptc_style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

triple_quote = ''' 
The "Policy to Code Generator" analyzes PDF documents to categorize policy topics, allowing users to select specific policies for automatic conversion into Rego code. This tool simplifies the translation of textual policies into executable rules for governance and compliance. It streamlines the process of policy enforcement in IT environments by generating code that directly aligns with organizational standards.'''
new_line = 'first line \n second line'

st.title("Policy to Code Generator")
st.sidebar.header("Policy to Code Generator", help=triple_quote)


uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    keywords = ["Access Control", "Network Standards", "RBAC", "Kubernetes", "Network Firewall", "IP Table",
            "Container Security"]
    topics = extract_specific_topics(pdf_text, keywords)

    topics_for_selection = ["Please select a topic"] + [(topic) for topic in topics]
    selected_topic = st.selectbox("Pick a Standard", topics_for_selection)

    if selected_topic == "Network Firewall":
        lang_format_options = ["Firewall Rules", "Rego Code"]
    elif selected_topic == "RBAC":
        lang_format_options = ["Access Control", "Rego Code"]
    else:
        lang_format_options = ["Rego Code"]
    
    if selected_topic != "Please select a topic":    
        langFormat = st.selectbox("Select the desired language format you want", lang_format_options)

        # if langFormat != "Rego Code":
        firewall_reference = st.file_uploader(f"Upload a {langFormat} Reference file", type=["txt", "pdf"])
        
        if st.button("Submit"):
            print("Button Clicked")
            st.info(f'{langFormat} is generating... Please Wait', icon="ℹ️")        

            response = generate_rego_and_firewall_rules(selected_topic, pdf_text, firewall_reference)
            if langFormat == "Rego Code":
                with st.expander("Rego Code"):
                    st.code(response[1])
            else:
                with st.expander("Firewall Rules"):        
                    st.write(response[2])


    # Use langchain_helper to extract topics and generate rego code