import streamlit as st
import ptc_langchain_helper as langchain_helper
import PyPDF2

st.title("Policy to Code Generator")
st.sidebar.header("Policy to Code Generator")
st.sidebar.markdown(''' 
The "Policy to Code Generator" analyzes PDF documents to categorize policy topics, allowing users to select specific policies for automatic conversion into Rego code. This tool simplifies the translation of textual policies into executable rules for governance and compliance. It streamlines the process of policy enforcement in IT environments by generating code that directly aligns with organizational standards.''')

# Allow user to upload a PDF file
def extract_text_from_pdf(file):
    text = ""
    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Allow user to upload a PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

    # st.subheader("Extracted Topics:")
    # st.write(pdf_text)

    # Use langchain_helper to extract topics and generate rego code
    response = langchain_helper.generate_topics_and_rego_code_from_pdf(pdf_text)

    # if response:
    #     # st.header(response['restaurant_name'].strip())
    #     rego_code = response['menu_items']
    #     st.write("**Rego Code**")
        # st.write("-", rego_code)



