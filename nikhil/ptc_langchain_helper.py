# ptc_langchain_helper.py
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
llm = ChatOpenAI(model="ft:gpt-3.5-turbo-0613:personal::8TSReyDR", temperature=0.7)

query_responses = []

def extract_specific_topics(pdf_text: str, keywords: list) -> List[str]:
    pdf_text_lower = pdf_text.lower()
    matched_topics = [keyword for keyword in keywords if keyword.lower() in pdf_text_lower]
    return matched_topics

def generate_rego_and_firewall_rules(topic, text, firewall_reference):
    global query_responses

    prompt_template_network = PromptTemplate(
        input_variables=['topic'],
        template=f"Given the {topic} standard, define the policy details such as name, type, subnet, security group, and firewall rules (if present) using the pdf."
    )

    network_chain = LLMChain(llm=llm, prompt=prompt_template_network, output_key="network_details")

    # Chain 2: Generate Rego Code
    prompt_template_rego = PromptTemplate(
        input_variables=['network_details'],
        template=f"You are an assistant that takes input as a policy and gives output as Rego code only. write a {topic} rego code and take its context from {text} if it's relatable to that topic otherwise take context from your own. Send only rego code."
    )

    rego_code_chain = LLMChain(llm=llm, prompt=prompt_template_rego, output_key="rego_code")

    # Chain 3: Generate Firewall Rules
    prompt_template_firewall = PromptTemplate(
        input_variables=['rego_code', 'firewall_reference'],
        template=f"Based on the generated Rego code and the Firewall Policy file uploaded, create rules which are in format of that suggest in the CLI Format only. Don't give any notes or explanation."
    )

    firewall_chain = LLMChain(llm=llm, prompt=prompt_template_firewall, output_key="firewall_rules")

    # Vectorize the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)

    # Embeddings
    embeddings = OpenAIEmbeddings()
    VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
    docs = VectorStore.similarity_search(query=f"{topic} Rego code", k=3)

    processed_text = docs[0]  # or a summary of docs[0]

    chain = SequentialChain(
        chains=[network_chain, rego_code_chain, firewall_chain],
        input_variables=['topic', 'processed_text', 'firewall_reference'],
        output_variables=["rego_code", "firewall_rules"]
    )

    input_data = {'topic': topic, 'processed_text': processed_text, 'firewall_reference': firewall_reference}
    response = chain(input_data)

    network_details = response.get("network_details", {})
    rego_code = response.get("rego_code", "")
    firewall_rules = response.get("firewall_rules", "")
    query_responses.append((f"{topic} Rego code", rego_code))
    query_responses.append((f"{topic} Firewall rules", firewall_rules))

    return network_details, rego_code, firewall_rules

def extract_text_from_pdf(file):
    text = ""
    if file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# def generate_topics_and_rego_code_from_pdf():
    
    # with st.form(key='my_form'):
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
        # else:
        # st.info("Please select a upload all the files and select options to generate the code.")