from pinecone import Pinecone, ServerlessSpec
from key import pineconeKey
from embeddings import get_embeddings
from story import get_chunks
import asyncio

pc = Pinecone(api_key=pineconeKey)
environment = "us-east-1-aws"
#index_list = pc.list_indexes()
index_name = "story-index"
index = pc.Index(index_name)
#vector_id = "text1"  #setting a unique vector id for this vector in vectorDB

#embeddings = get_embeddings(text=text1)


async def insert_embeddings(embeddings, metaData, vectorId):
    try:
        await index.upsert(
            vectors=[
                {
                    'id':vectorId,
                    'values':embeddings,
#                    'metadata':{'about': metaData}
                     'metadata':metaData,
                }
            ]
        )
    except Exception as e:
        print(f"An error occured during insertion: {e}")

async def get_chunk_embeddings():
    chunks = get_chunks()
    count = 0
    all_embeddings = []
    for chunk in chunks:
        print(f"Requested embeddings for chunk {count}")
        embeddings = get_embeddings(text=chunk)
        count += 1
        all_embeddings.append(embeddings)
    all_embeddings1 = await asyncio.gather(*all_embeddings)
#    all_embeddings = await asyncio.gather(*[get_embeddings(chunk) for chunk in chunks])
    return all_embeddings1

async def store_chunk_embeddings():
    all_embeddings = await get_chunk_embeddings()
    count = 1
    tasks = []
    for embeddings in all_embeddings:
        task = insert_embeddings(embeddings=embeddings, metaData=f'chunk{count}', vectorId=f'chunk{count}')
        print(f"Inserted embeddings for chunk {count}")
        count += 1
        tasks.append(task)
    await asyncio.gather(*tasks)
    print("DONE for all chunks.")


asyncio.run(store_chunk_embeddings())