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

def check_compliance_with_gpt35(policy_text,code_text):
    global query_responses
    query = f"Your an rego code policy validator you job is to check if the policy code compliance the policy and detail explain of why it doesn't adhere List down the policy and tell if it is Compliance or not\n\nPolicy:\n{policy_text}\n\nCode:\n{code_text} if the {policy_text} doesn't found with even a single one in {code_text} says it is not relavant file policy's doesn't replicate in the policy code, give me output in this format 3 columns this is an example don't replicate in the output 1st column Policy Statement 2nd column for Compliance if it Yes or No only 3rd column for Detailed Reason with the Line Number it is referring. For Each Policy should be in a table format no explanation only the table only strictly don't ever give the explanation or note only the table"
    
    for stored_query, response in query_responses:
        if query == stored_query:
            return {"issue": response,"count":response}
    
    openai_response_gpt35 = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        temperature=0.7,
        prompt=query,
        max_tokens=1000
    )

    choices = openai_response_gpt35.choices

    openai_output = choices[0].text
    
    query_responses.append((query,openai_output))
    print(query_responses)
    
    return {"issue": openai_output,"count":openai_output} 

def check_compliance_with_openai(policy_text, code_text):
    # Use OpenAI to compare policy and code
    # Implement your OpenAI API call logic for code comparison
    global query_responses
    query = f"Your an rego code policy validator you job is to check if the policy code compliance the policy and detail explain of why it doesn't adhere List down the policy and tell if it is Compliance or not\n\nPolicy:\n{policy_text}\n\nCode:\n{code_text} if the {policy_text} doesn't found with even a single one in {code_text} says it is not relavant file policy's doesn't replicate in the policy code, give me output in this format 3 columns this is an example don't replicate in the output 1st column Policy Statement 2nd column for Compliance if it Yes or No only 3rd column for Detailed Reason with the Line Number it is referring. For Each Policy should be in a table format no explanation only the table only strictly don't ever give the explanation or note only the table"
    
    for stored_query, response in query_responses:
        if query == stored_query:
            return {"issue": response,"count":response}
    
    openai_response = client.chat.completions.create(  # Use the chat endpoint
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content":query,
        }
        ]
    )
    openai_output = openai_response.choices[0].message.content
        
    query_responses.append((query,openai_output))
    print(query_responses)
    

    return {"issue": openai_output,"count":openai_output}