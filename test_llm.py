from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv(""),
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Suggest a career for a Python developer interested in AI"}
    ]
)

print(response.choices[0].message.content)