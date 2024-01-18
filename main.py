# # main.py
#
# import streamlit as st
# import langchain_helper
# import PyPDF2
#
# st.title("Policy to Code Generator")
#
#
# # Allow user to upload a PDF file
# def extract_text_from_pdf(file):
#     text = ""
#     if file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]
#             text += page.extract_text()
#     return text
#
#
# # Allow user to upload a PDF file
# uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
#
# if uploaded_file:
#     # Extract text from the uploaded PDF
#     pdf_text = extract_text_from_pdf(uploaded_file)
#
#     # Display extracted text to the user
#     # st.subheader("Extracted Text from PDF:")
#     # st.text(pdf_text)
#
#     # Use langchain_helper to extract topics
#     topics = langchain_helper.extract_topics_using_ai(pdf_text)
#
#     # Display topics to the user
#     # st.subheader("Extracted Topics:")
#     # st.write(topics)
#
#     # Allow user to pick a standard from the extracted topics
#     cuisine = st.sidebar.selectbox("Pick a Standard", topics)
#
#     if cuisine:
#         response = langchain_helper.generate_restaurant_name_and_items(cuisine)
#         st.header(response['restaurant_name'].strip())
#         menu_items = response['menu_items']
#         st.write("**Rego Code**")
#         st.write("-", menu_items)



# main.py

import streamlit as st
import langchain_helper
import PyPDF2

st.title("Policy to Code Generator")


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

    if response:
        # st.header(response['restaurant_name'].strip())
        rego_code = response['menu_items']
        # st.write("**Rego Code**")
        # st.write("-", rego_code)



