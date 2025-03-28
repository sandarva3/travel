import google.generativeai as genai
from .key import googleKey
#import time

def send_to_gemini(prompt):
    
    genai.configure(api_key=googleKey)
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Sending to Gemini...")
        response = model.generate_content(prompt)
        print("Got gemini response.")
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"
    #print("THE REPONSE FROM GEMINI: ")
    #response = response.text
    #if response:
    #    for i in response:
    #        print(i, end="", flush=True)
    #        time.sleep(0.01)
    #else:
    #    print("NO response from gemini")