from google import genai
from google.genai import types
#import google.generativeai as genai
import json
from key import googleKey
import time


client = genai.Client(api_key=googleKey)
# Load your JSON file
with open('output.json', 'rb') as f:
    json_data = f.read()

prompt = "Analyze this JSON data. Tell me what it's about. Also: Give me the names of places there, keep in mind only name, nothing else. \
Like name1: 'name of place 1, name2:'name of place2' etc.  Important: EVen if places are duplicated, keep printing, all place's name. \
EXTREMELY IMPORTANT: after doing it, search the internet about 'Pashupatinath Temple, Kathmandu' and give me its summary in 7 sentences. \
Also tell me did you searched the web? how much websites? and did you read things about it from those websites and generated me the compact summary?"
print("Sending to Gemini...")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(
            data=json_data,
            mime_type='text/plain',
        ),
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