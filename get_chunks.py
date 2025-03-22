from pinecone import Pinecone, ServerlessSpec
from key import pineconeKey
from embeddings import get_embeddings
from story import get_chunks
import asyncio



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
best_chunk = top_chunks[0]
print("The best chunk is:")
print(best_chunk)