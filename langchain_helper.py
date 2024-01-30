import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

import os

os.environ['OPENAI_API_KEY'] = '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'  # Replace with your OpenAI API key

llm = ChatOpenAI(model="ft:gpt-3.5-turbo-0613:personal::8TSReyDR", temperature = 0.7)

query_responses = []



def extract_specific_topics(pdf_text: str, keywords: list) -> List[str]:
    pdf_text_lower = pdf_text.lower()
    matched_topics = [keyword for keyword in keywords if keyword.lower() in pdf_text_lower]
    return matched_topics

def extract_topics_using_ai(pdf_text: str) -> List[str]:
    # Use generative AI to extract topics from the PDF text
    # Implement the logic based on your requirements using langchain or other methods
    # Placeholder logic: Split the text into paragraphs and treat each paragraph as a topic
    topics = [topic.strip() for topic in pdf_text.split('\n') if topic.strip()]
    return topics


def generate_rego_code_for_topic(topic, text):
    
    global query_responses
    # Check if query already exists in stored responses
    
        
    prompt_template_network = PromptTemplate(
        input_variables=['topic'],
        template=f"Given the {topic} standard, define the policy details such as name, type, subnet, security group, and firewall rules(if present) using the pdf."
    )

    network_chain = LLMChain(llm=llm, prompt=prompt_template_network, output_key="network_details")
    query = f"You are an assistant that takes input as a policy and gives output as Rego code only. write a {topic} rego code and take its context from {text} if it's relatable to that topic otherwise take context from your own. Send only rego code."
    
    for stored_query, response in query_responses:
        if query == stored_query:
            # Return the stored response for the existing query
            return query,response   
    # Chain 2: Generate Rego Code
    prompt_template_rego = PromptTemplate(
        input_variables=['network_details'],
        template=f"You are an assistant that takes input as a policy and gives output as Rego code only. write a {topic} rego code and take its context from {text} if it's relatable to that topic otherwise take context from your own. Send only rego code."
    )

    rego_code_chain = LLMChain(llm=llm, prompt=prompt_template_rego, output_key="rego_code")

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
    docs = VectorStore.similarity_search(query=query, k=3)
    # print(docs)
    # Add vectorized text to the input for the chains
    processed_text = docs[0]  # or a summary of docs[0]

    # Ensure the processed text is within the token limit
    # You may need to truncate or further summarize the text here

    # Create the SequentialChain with adjusted input
    chain = SequentialChain(
        chains=[network_chain, rego_code_chain],
        input_variables=['topic', 'processed_text'],
        output_variables=["rego_code"]
    )

    # Execute the chain with the input data
    input_data = {'topic': topic, 'processed_text': processed_text}
    response = chain(input_data)
    # Retrieve the results
    network_details = response.get("network_details", {})
    rego_code = response.get("rego_code", "")
    query_responses.append((query, rego_code))

    # Return the results
    return network_details, rego_code

def generate_topics_and_rego_code_from_pdf(pdf_text):
    keywords = ["access control", "network standards", "rbac", "kubernetes", "network"]
    topics = extract_specific_topics(pdf_text, keywords)

    #Convert topics to a format suitable for user selection
    topics_for_selection = ["Please select a topic"] + [(topic) for topic in topics]

    #Allow the user to select a topic
    selected_topic = st.sidebar.selectbox("Pick a Standard", topics_for_selection)

    #Check if a topic is selected
    if selected_topic != "Please select a topic":
        # Use the selected topic to generate rego code
        response = generate_rego_code_for_topic(selected_topic, pdf_text)
        
        # Display the rego code
        # st.header(response[0].strip())  # Access the first element of the tuple (standard_name)
        menu_items = response[1]
        st.write("**Rego Code**")
        st.code(menu_items)
        # print(query_responses[1])
        # print(menu_items)
    else:
        st.info("Please select a topic to generate the rego code.")

if __name__ == "__main__":
    pdf_text_example = "This is a sample PDF text with multiple topics.\nTopic 1: Network Standards\nTopic 2: RBAC\nTopic 3: Access Control\nTopic 4: Kubernetes"
    generate_topics_and_rego_code_from_pdf(pdf_text_example)



