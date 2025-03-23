import google.generativeai as genai
from key import googleKey
import time


def send_gemini(chunks, question):


    genai.configure(api_key=googleKey)

    prompt = f"""CONTEXT CHUNKS: {{      {chunks}        }}.
  The question: {{    {question}  }}. EXTREMELY IMPORTANT: USE CHUNKS FOR CONTEXT AND ANSWER THE GIVEN QUESTION PROPERLY BY DESCRIBING IN PARAGRAPH(not points). 
  DON'T SAY ANY OTHER THING, JUST ANSWER QUESTION."""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Sending to Gemini...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"
'''
url = "https://roomapp.pythonanywhere.com/media/lanmedia/InTheBeginningWasCommandLine.txt"
response = send_gemini(url)
print("THE REPONSE FROM GEMINI: ")
if response:
    for i in response:
        print(i, end="", flush=True)
        time.sleep(0.01)
else:
    print("NO response from gemini")
'''