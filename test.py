from openai import OpenAI as openai
from dotenv import load_dotenv

load_dotenv()
client=openai()


openai_response_gpt35 = client.completions.create(
    model="gpt-3.5-turbo-instruct",
        temperature=0.7,
        prompt="Hello what is your response",
        max_tokens=1000
)

choices = openai_response_gpt35.choices

response_text = choices[0].text

# Print the response text
print(response_text)