from google import genai
from google.genai import types
#import google.generativeai as genai
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


def get_conv_history():
    with open("conv_history.txt", "r") as file:
        file_data = file.read()
    return file_data
        

def save_conv(chat):
    with open("conv_history.txt", 'a', encoding="utf-8") as file:
        file.write(chat)


def chat():
    chat_string = ""
    count = 1
    while True:
        inp = input("You: ")
        if inp == "0":
            print("ENDING CONVERSATION...")
            break
        prompt = f"""You are an AI assistant. Answer user queries accurately and intelligently.  
Use the following past conversation only for relevant context—do not mention or reference it in your response.  

PAST CONVERSATION: {{   {get_conv_history()}  }}

USER PROMPT: {{   {inp}   }} 

RULES:  
- If the past conversation contains relevant context, use it to improve your answer.  
- If no relevant context exists, respond as if this is a new question.  
- NEVER mention past conversations, context usage, or lack of information.  
- Your response should be clear, logical, and direct. Avoid unnecessary filler.  
"""
  

        response = talk_gemini(prompt=prompt)
        print_response(response=response)
        chat_string = f"""-User: {inp}
-Assistant: {response}"""
        save_conv(chat_string)
        count += 1


chat()

'''
 '''