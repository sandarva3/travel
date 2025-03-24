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
def talk_gemini(prompt):
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
    return response.text


def print_response(response):
    print("Gemini: ", end="")
    for i in response:
        print(i, end="", flush=True)
        time.sleep(0.01)

def save_conv(conv):
    with open("conv_history.json", 'w', encoding="utf-8") as file:
        file.write(conv)

past_conv = {}
json_string = ""
conv_string = ""
def chat():
    global json_string
    count = 1
    while True:
        inp = input("You: ")
        if inp == 0:
            print("ENDING CONVERSATION...")
            break
        prompt = f"""You are an AI assistant. Answer user queries accurately and intelligently.  
Use the following past conversation only for relevant context—do not mention or reference it in your response.  

PAST CONVERSATION: {json.dumps(past_conv, indent=2)}  

USER PROMPT: {inp}  

RULES:  
- If the past conversation contains relevant context, use it to improve your answer.  
- If no relevant context exists, respond as if this is a new question.  
- NEVER mention past conversations, context usage, or lack of information.  
- Your response should be clear, logical, and direct. Avoid unnecessary filler.  
"""
  

        response = talk_gemini(prompt=prompt)
        print_response(response=response)
        past_conv[f'{count}.me'] = inp
        past_conv[f'{count}.you'] = response
        json_string = json.dumps(past_conv, indent=2, ensure_ascii=False)
        save_conv(json_string)
        count += 1


chat()

'''
 How much of a request can I make to you through an API call. I'm making a software and I want to make you a parallel request on different topic, the problem is requesting you one by one for each topic would be very time consuming. can i make parallel request to you? i can. and i have. but it's through threading in python. like i used .to_thread() method of asyncio in python. but the problem is: when i made 22 parallel request to you at once, simulataneously, you were only able to answer for only 20 of them. is there limit for that? for eg, i might might 60 parallel request to you at once simultenously, how can I handle that?
'''