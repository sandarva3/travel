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

prompt = """EXTREMELY IMPORTANT: Scan this url: 'https://roomapp.pythonanywhere.com/media/lanmedia/InTheBeginningWasCommandLine_9pOyVim.txt' .\
and summarize me what's discussed there. 
After you do that also tell me: 
0) When was that written? Author says the date of writing, when was it?? 
1) Author discusses his friend's dad car in the essay, which car was that?? 
2) how did you scan the url's file?? like a prompt or how?? 
3) plus, when you scan it, does it count on my part? like is my tokens usage taken when you process that whole data?
 like is my tokens cut from doing that as well?? 
or is it completely on your part and my tokens are not cut when you process that data given in a url???? 
4) I know my tokens are cut from my prompt, but is it also cut from the url's data? 
5) I provide you reference to data through url, not the actual data. so when you do your part to fetch that actual data through url, does processing that actual data \
also cut my tokens or not??? 
6) TELL HONESTLY: Did you searched the web or did you accessed the file from the url that I provided? """
print("Sending to Gemini...")
response = client.models.generate_content(
    model="gemini-1.5-flash",
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