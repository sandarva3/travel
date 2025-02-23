import google.generativeai as genai
import asyncio
from key import googleKey
import time

genai.configure(api_key=googleKey)

async def check(num):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"What's this number: {num}. Answer in: 'Number is: <number>.'"

    print(f"Sending request for number: {num}")
    response = await model.generate_content_async(prompt)
    
    print(f"Gemini responded for number: {num}")
    return response.candidates[0].content

async def main():
    numbers = [1, 2, 3, 4, 5, 6, 7]

    responses = await asyncio.gather(*[check(num) for num in numbers])

    for response in responses:
        for i in response:
            print(i, end='', flush=True)
            time.sleep(0.02)

asyncio.run(main())







'''

from google import genai
#import google.generativeai as genai
from key import googleKey
import time
import asyncio


async def check(num):
    client = genai.Client(api_key=googleKey)
    prompt = f"What's this number: {num}. Answer in: 'Number is: <number>.'"
    print(f"Sending request for num: {num}")
    response = await client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    print(f"Gemini responded for number: {num}")
    return response.text


async def main():
    numbers = [1,2,3,4,5,6,7]
    responses = await asyncio.gather(*[check(num) for num in numbers])

    for response in responses:
        for i in response:
            print(i, end="", flush=True)
            time.sleep(0.02)


asyncio.run(main())


'''