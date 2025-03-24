from google import genai
from google.genai import types
#import google.generativeai as genai
import json
from key import googleKey
import time


client = genai.Client(api_key=googleKey)
# Load your JSON file
#with open('output.json', 'rb') as f:
#    json_data = f.read()
def talk(prompt):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            # types.Part.from_bytes(
            #     data=json_data,
            #     mime_type='text/plain',
            # ),
            prompt
        ]
    )
    print("THE REPONSE FROM GEMINI: ")
    response = response.text
    if response:
        for i in response:
            print(i, end="", flush=True)
            time.sleep(0.01)
    else:
        print("NO response from gemini")

def chat():
    while True:
        inp = input("You: ")
        if inp == 0:
            break
        talk("""Past Conversation: {You: Hey?
THE REPONSE FROM GEMINI: 
Hey there! How can I help you today?
You: How you doing?    
THE REPONSE FROM GEMINI: 
I'm doing well, thank you for asking!  How are you?
You: fine.
THE REPONSE FROM GEMINI: 
Okay.  Is there anything I can help you with?
You: i'm from lalitpur, nepal.
THE REPONSE FROM GEMINI: 
That's great! Lalitpur is a beautiful city.  Is there anything specific you'd like to talk about regarding Lalitpur, Nepal?  Perhaps you have a question, or you'd like to share something about your experiences there?
You: where i am from?
}. New user prompt:{tell me where am I from?} RULE: don't say mention anything to user of past convesation, use past conversation for context and just answer to user.""")

chat()

'''
link1 = "https://roomapp.pythonanywhere.com/media/lanmedia/output.json"
link2 = "https://roomapp.pythonanywhere.com/media/lanmedia/dbms_lab6.txt"

def Whatsup(prompt):
    genai.configure(api_key=googleKey)

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Generating response from Gemini...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"

prompt = f"Analyze this JSON data, and text data. LINKS: link1 = {link1}, link2 = {link2} . Tell me what it's about. Also: Give me the names of places there of json data as well. \
keep in mind only name, nothing else. Like name1: 'name of place 1, name2:'name of place2' etc. Also after doing that, tell me, how did you \
got both datas? as a file or directly embedded in prompt?? or did you accessed it from URL yourself? If You accessed it from url, tell me how you did it as well \
What if I want to send data 5x that amount of size? can you still process it if I provide you the link?? \
As when you process like this through a link, how do you process it? like a file?? or prompt??"

response = Whatsup(prompt)

if response:
    print(f"RESPONSE FROM GEMINI")
    for i in response:
        print(i, end="", flush=True)
        time.sleep(0.05)
else:
    print("NO RESPONSE FROM GEMINI")

'''