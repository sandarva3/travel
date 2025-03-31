from google import genai
from .key import googleKey


def ask_gemini_places_recommendation(prompt):
    client = genai.Client(api_key=googleKey)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt
        ]
    )
    return response.text