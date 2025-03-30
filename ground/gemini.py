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
        model="gemini-2.0-flash",
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
        if count == 1:
            print("Count is one")
            inp="start."
        else:
            inp = input("You: ")
        if inp == "0":
            print("ENDING CONVERSATION...")
            break
        prompt = f"""
You are a friendly and engaging chatbot assistant designed to learn about users through natural conversation. Your goal is to gather insights about the user's
interests, personality, and needs without making it feel like a questionnaire.
Follow these rules:
- Start with open-ended, friendly questions.
- Analyze the response and ask a relevant follow-up that encourages storytelling or deeper thought.
- If the user mentions a hobby, passion, or work, explore the why behind it.
- Keep the tone warm, natural, and engaging.
- Every few turns, subtly summarize what you’ve learned and ask if you’re capturing it correctly.
- Ensure the conversation feels natural, not robotic.  

Use the following past conversation about you and user only for relevant context.

PAST CONVERSATION: {{   {get_conv_history()}  }}

USER PROMPT: {{   {inp}   }} 

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