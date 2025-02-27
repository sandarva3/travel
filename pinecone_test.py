from pinecone import Pinecone, ServerlessSpec
from key import pineconeKey

pc = Pinecone(api_key=pineconeKey)

environment = "us-east-1-aws"
index_list = pc.list_indexes()

index_name = "story-index"

index = pc.Index(index_name)
