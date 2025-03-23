from pinecone import Pinecone, ServerlessSpec
from key import pineconeKey
from embeddings import get_embeddings
from story import get_chunks
import asyncio
import time
from gemini11 import send_gemini



pc = Pinecone(api_key=pineconeKey)

index_name = "story-index"
index = pc.Index(index_name)


query = input("Enter a question: ")

query_embeddings = get_embeddings(query)
print("Querying the pinecone...")
response = index.query(vector=query_embeddings, top_k=3, include_metadata=True)
print("Queried the pinecone.")
top_chunks = [chunks for chunks in response["matches"]]

print("Best matching chunk: ")
print(top_chunks)

print("sending question to gemini.")

response = send_gemini(top_chunks, query)
print("THE REPONSE FROM GEMINI: ")
if response:
    for i in response:
        print(i, end="", flush=True)
        time.sleep(0.01)
else:
    print("NO response from gemini")