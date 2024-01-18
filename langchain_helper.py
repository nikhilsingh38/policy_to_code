# # langchain_helper.py
# import streamlit as st
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from langchain.chains import SequentialChain
# from secret_key import openapi_key
#
# import os
# os.environ['OPENAI_API_KEY'] = openapi_key
#
# llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.7)
#
# def extract_topics_using_ai(pdf_text):
#     # Use generative AI to extract topics from the PDF text
#     # Implement the logic based on your requirements using langchain or other methods
#     # Placeholder logic: Split the text into paragraphs and treat each paragraph as a topic
#     topics = [topic.strip() for topic in pdf_text.split('\n') if topic.strip()]
#     return topics
#
# def generate_from_pdf(pdf_text):
#     # Use the pdf_text to fetch the standard name and generate rego code
#     # Implement the logic based on your requirements
#     # For now, let's return a placeholder response
#     return {"standard_name": "Generated Standard Name", "menu_items": ["Item 1", "Item 2"]}
#
# def generate_restaurant_name_and_items(cuisine):
#     # Chain 1: Restaurant Name
#     prompt_template_name = PromptTemplate(
#         input_variables=['cuisine'],
#         template="I want to create a a one word standard name from open policy agent for {cuisine} standard. The result should be in one word"
#     )
#
#     name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")
#
#     # Chain 2: Menu Items
#     prompt_template_items = PromptTemplate(
#         input_variables=['restaurant_name'],
#         template="""create a proper rego code for {restaurant_name} based on Open policy agent. Return it as a rego code format"""
#     )
#
#     food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")
#
#     chain = SequentialChain(
#         chains=[name_chain, food_items_chain],
#         input_variables=['cuisine'],
#         output_variables=['restaurant_name', "menu_items"]
#     )
#
#     response = chain({'cuisine': cuisine})
#
#     return response
#
# def generate_topics_and_cuisine_from_pdf(pdf_text):
#     # Extract topics using generative AI
#     topics = extract_topics_using_ai(pdf_text)
#
#     # Convert topics to a format suitable for user selection
#     topics_for_selection = [(topic, topic) for topic in topics]
#
#     # Allow user to select a topic
#     selected_topic = st.sidebar.selectbox("Pick a Topic", topics_for_selection)
#
#     # Use selected topic to generate restaurant name and items
#     response = generate_restaurant_name_and_items(selected_topic)
#
#     return response
#
# if __name__ == "__main__":
#     # Example usage
#     pdf_text_example = "This is a sample PDF text with multiple topics.\nTopic 1: Network Standards\nTopic 2: RBAC\nTopic 3: Access Control\nTopic 4: Kubernetes"
#     response = generate_topics_and_cuisine_from_pdf(pdf_text_example)
#     print(response)




# langchain_helper.py

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from typing import List

import os

os.environ['OPENAI_API_KEY'] = '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'  # Replace with your OpenAI API key

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.7)

def extract_specific_topics(pdf_text: str, keywords: list) -> List[str]:
    # Convert the PDF text to lowercase for case-insensitive matching
    pdf_text_lower = pdf_text.lower()

    # Find topics that contain any of the specified keywords
    matched_topics = [keyword for keyword in keywords if keyword.lower() in pdf_text_lower]

    return matched_topics

def extract_topics_using_ai(pdf_text: str) -> List[str]:
    # Use generative AI to extract topics from the PDF text
    # Implement the logic based on your requirements using langchain or other methods
    # Placeholder logic: Split the text into paragraphs and treat each paragraph as a topic
    topics = [topic.strip() for topic in pdf_text.split('\n') if topic.strip()]
    return topics

# langchain_helper.py

def generate_rego_code_for_topic(topic, text):
    # Chain 1: Define Network Details
    prompt_template_network = PromptTemplate(
        input_variables=['topic'],
        template=f"Given the {topic} standard, define the policy details such as name, type, subnet, security group, and firewall rules(if present) using the pdf."
    )

    network_chain = LLMChain(llm=llm, prompt=prompt_template_network, output_key="network_details")

    # Chain 2: Generate Rego Code
    prompt_template_rego = PromptTemplate(
        input_variables=['network_details'],
        template=f"You are an assistant that takes input as a policy and gives output as Rego code only. write a {topic} rego code and take its context from {text} if its is relatable to that topic otherwise take context from your own. Send only rego code."
    )

    rego_code_chain = LLMChain(llm=llm, prompt=prompt_template_rego, output_key="rego_code")

    chain = SequentialChain(
        chains=[network_chain, rego_code_chain],
        input_variables=['topic'],
        output_variables=["rego_code"]
    )

    response = chain({'topic': topic})

    return response.get("network_details", {}), response.get("rego_code", "")


def generate_topics_and_rego_code_from_pdf(pdf_text):
    # Specify the keywords you want to match
    keywords = ["access control", "network standards", "rbac", "kubernetes", "network"]

    # Extract specific topics using predefined keywords
    topics = extract_specific_topics(pdf_text, keywords)

    # Convert topics to a format suitable for user selection
    topics_for_selection = ["Please select a topic"] + [(topic) for topic in topics]

    # Allow the user to select a topic
    selected_topic = st.sidebar.selectbox("Pick a Standard", topics_for_selection)

    # Check if a topic is selected
    if selected_topic != "Please select a topic":
        # Use the selected topic to generate rego code
        response = generate_rego_code_for_topic(selected_topic, pdf_text)

        # Display the rego code
        # st.header(response[0].strip())  # Access the first element of the tuple (standard_name)
        menu_items = response[1]
        st.write("**Rego Code**")
        st.write("-", menu_items)
    else:
        # Display a default message prompting the user to select a topic
        st.info("Please select a topic to generate the rego code.")

if __name__ == "__main__":
    pdf_text_example = "This is a sample PDF text with multiple topics.\nTopic 1: Network Standards\nTopic 2: RBAC\nTopic 3: Access Control\nTopic 4: Kubernetes"
    generate_topics_and_rego_code_from_pdf(pdf_text_example)



