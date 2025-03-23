import google.generativeai as genai
import asyncio
import time
from key import googleKey  # Ensure this exists

genai.configure(api_key=googleKey)

# Function to generate response (must run in a thread)
async def check(num):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Hey, what's up? how you doing??? What's this number: {num}?"

    print(f"Sending request for number: {num}")
    
    # Run the synchronous API in a separate thread
    response = await asyncio.to_thread(model.generate_content, prompt)
    
    print(f"Gemini responded for number: {num}")
    return response.text

# Main async function
async def main():
    numbers = [1, 2, 3, 4, 5, 6, 7]
    
    # Run requests in parallel
    responses = await asyncio.gather(*[check(num) for num in numbers])
    
    # Print results with animated effect
    for response in responses:
        for char in response:
            print(char, end="", flush=True)
            time.sleep(0.02)

# Run the async event loop
asyncio.run(main())
