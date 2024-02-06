import streamlit as st
import ptc_langchain_helper as langchain_helper
import PyPDF2


st.set_page_config(page_title="Policy to Code", page_icon="📈",layout="wide")

# st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">', unsafe_allow_html=True)

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

with open('./ptc_style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


triple_quote = ''' 
The "Policy to Code Generator" analyzes PDF documents to categorize policy topics, allowing users to select specific policies for automatic conversion into Rego code. This tool simplifies the translation of textual policies into executable rules for governance and compliance. It streamlines the process of policy enforcement in IT environments by generating code that directly aligns with organizational standards.'''
new_line = 'first line \n second line'

st.title("Policy to Code Generator")
st.sidebar.header("Policy to Code Generator", help=triple_quote)
# st.sidebar.markdown(''' 
# The "Policy to Code Generator" analyzes PDF documents to categorize policy topics, allowing users to select specific policies for automatic conversion into Rego code. This tool simplifies the translation of textual policies into executable rules for governance and compliance. It streamlines the process of policy enforcement in IT environments by generating code that directly aligns with organizational standards.''')

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



