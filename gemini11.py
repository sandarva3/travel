import google.generativeai as genai
from key import googleKey
import time


def send_gemini(url):
    """
    Ranks professionals based on user data using Google AI's Gemini model.

    Args:
        user_data (str): JSON string containing user data.
        prof_data (str): JSON string containing professional data.

    Returns:
        str: IDs of matching professionals.
    """
    genai.configure(api_key=googleKey)

    prompt = f"EXTREMELY IMPORTANT: Scan this url: '{url}' . and summarize me what's discussed there. \
After you do that also tell me: \
0) When was that written? Author says the date of writing, when was it?? \
1) Author discusses his friend's dad car in the essay, which car was that?? \
2) how did you scan the url's file?? like a prompt or how?? \
3) plus, when you scan it, does it count on my part? like is my tokens usage taken when you process that whole data? like is my tokens cut from doing that as well?? \
or is it completely on your part and my tokens are not cut when you process that data given in a url???? \
4) I know my tokens are cut from my prompt, but is it also cut from the url's data? \
5) I provide you reference to data through url, not the actual data. so when you do your part to fetch that actual data through url, does processing that actual data \
also cut my tokens or not??? " 

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        print("Sending to Gemini...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "Error generating response"

url = "https://roomapp.pythonanywhere.com/media/lanmedia/InTheBeginningWasCommandLine.txt"
response = send_gemini(url)
print("THE REPONSE FROM GEMINI: ")
if response:
    for i in response:
        print(i, end="", flush=True)
        time.sleep(0.01)
else:
    print("NO response from gemini")