import google.generativeai as genai
import json
from key import googleKey


def Whatsup(prompt):
    genai.configure(api_key=googleKey)

#    prompt = f"
#    Hey, how you doin?? 
#    Which model you are? 1.5 or 2.0?
#    "

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Generating response from Gemini...")
        response = model.generate_content(prompt)
        print(f"RESPONSE: {response.text.strip()}")
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"

while(True):
    prompt  = input("YOU: ")
    Whatsup(prompt)