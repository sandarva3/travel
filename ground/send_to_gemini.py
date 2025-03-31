import google.generativeai as genai
from .key import googleKey
import time
import random

MAX_RETRIES = 5  # Limit the number of retries
INITIAL_BACKOFF = 2  # Start with a 2-second wait


def send_to_gemini(prompt):
    genai.configure(api_key=googleKey)
    retries = 0
    backoff = INITIAL_BACKOFF

    while retries < MAX_RETRIES:
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            print(f"Attempt {retries + 1}: Sending to Gemini...")
            response = model.generate_content(prompt)
            print("Got Gemini response.")
            return response.text

        except Exception as e:
            if "429" in str(e):
                print(f"RATE LIMIT EXCEEDED. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                retries += 1
                backoff *= 2  # Exponential backoff
            else:
                print(f"Error generating response: {str(e)}")
                break  # Stop retrying if it's not a rate limit issue

    return "Error generating response after multiple retries as well."










"""

def send_to_gemini(prompt):
    
    genai.configure(api_key=googleKey)
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Sending to Gemini...")
        response = model.generate_content(prompt)
        print("Got gemini response.")
        return response.text
    except Exception as e:
        print(f"In ground/send_to_gemini.send_to_gemini() Error generating response: {str(e)}")
        return "Error generating response"
    



    #print("THE REPONSE FROM GEMINI: ")
    #response = response.text
    #if response:
    #    for i in response:
    #        print(i, end="", flush=True)
    #        time.sleep(0.01)
    #else:
    #    print("NO response from gemini")"

"""