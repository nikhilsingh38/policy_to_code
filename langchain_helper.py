# langchain_helper.py

from openai import OpenAI as openai
import PyPDF2
from dotenv import load_dotenv


# Set your OpenAI API key here
# openai.api_key = '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'
load_dotenv()
client=openai()

query_responses = []

def extract_text_from_file(file):
    # Implement text extraction logic from the file (PDF or text)
    # You can use PyPDF2 for PDF files and handle text files accordingly

    file_extension = file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(file)
    elif file_extension == "txt":
        return extract_text_from_text_file(file)
    else:
        # Handle other file types if needed
        return ""

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def extract_text_from_text_file(file):
    return file.read()

def check_compliance_with_openai(policy_text, code_text):
    # Use OpenAI to compare policy and code
    # Implement your OpenAI API call logic for code comparison
    global query_responses

    openai_response = client.chat.completions.create(  # Use the chat endpoint
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content":f"Your an rego code policy validator you job is to check if the rego code compliance the policy and detail explain of why it doesn't adhere List down the policy and tell if it is Compliance or not\n\nPolicy:\n{policy_text}\n\nCode:\n{code_text} if the {policy_text} doesn't found with even a single one in {code_text} says it is not relavant file policy's doesn't replicate in the rego code, give me output in this format 3 columns this is an example don't replicate in the output 1st column Policy Statement 2nd column for Compliance if it Yes or No 3rd column for Reason with the Line Number it is referring. For Each Policy should be in a table format no explanation only the table only strictly don't ever give the explanation only the table",
        }
        ]
    )
    
    # countofadhere = client.chat.completions.create(  # Use the chat endpoint
    # model="gpt-4",
    # messages=[
    #     {
    #         "role": "system",
    #         "content":f"Your an rego code policy validator you job is to check if the rego code adhere or doesn't adhere Give me an count of much Adhere or not \n\nPolicy:\n{policy_text}\n\nCode:\n{code_text} give me output in this format Adhere: 2 Doesn't: 1  give output as a python dictionary it is an example don't replicate Don't give any explaination only the list output strictly",
    #     }
    #     ]
    # )
    # openai_response = openai.Completion.create(
    #     engine="gpt-3.5-turbo-instruct",
    #     temperature=0.7,
    #     prompt=f"Your an rego code policy validator you job is to check if the rego code adhere the policy and detail explain of why it doesn't adhere List down the policy and tell if it is Adhere or not\n\nPolicy:\n{policy_text}\n\nCode:\n{code_text} give me output in this format this is an example don't replicate in the output 1. Policy Statement - Adhere 2. Policy Statement - Doesn't Adhere and another column for why it doesn't adhere, For Each Policy in a table format strictly",
    #     max_tokens=1000
    # )
    # countofadhere = client.chat.completions.create(
    #     engine="gpt-3.5-turbo-instruct",
    #     temperature=0.7,
    #     prompt=f"Your an rego code policy validator you job is to check if the rego code adhere the policy and detail explain of why it doesn't adhere Give me an count of much Adhere or not \n\nPolicy:\n{policy_text}\n\nCode:\n{code_text} give me output in this format this is an example don't replicate in the output Adhere: 2 Not Adhere: 1 ",
    #     max_tokens=1000
    # )

    # Extract the OpenAI response and determine compliance
    print (openai_response)
    openai_output = openai_response.choices[0].message.content
    
    for stored_query, response in query_responses:
        if query == stored_query:
            # Return the stored response for the existing query
            return query,response
    # count = countofadhere.choices[0].message.content
    # print(count)
    # compliant = "compliant" in openai_output.lower()

    return {"issue": openai_output,"count":openai_output}