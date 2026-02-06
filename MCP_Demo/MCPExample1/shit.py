import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# The client automatically picks up the API key from the environment variable
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="How does AI work?"
)

print(response.text)
