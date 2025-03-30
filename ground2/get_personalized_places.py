from google import genai
from .key import googleKey


client = genai.Client(api_key=googleKey)
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt
        ]
    )
    return response.text