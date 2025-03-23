from pinecone import Pinecone, ServerlessSpec
from key import pineconeKey
from embeddings import async_get_embeddings
from story import get_chunks
import asyncio

pc = Pinecone(api_key=pineconeKey)
environment = "us-east-1-aws"
#index_list = pc.list_indexes()
index_name = "story-index"
index = pc.Index(index_name)
#vector_id = "text1"  #setting a unique vector id for this vector in vectorDB

#embeddings = async_get_embeddings(text=text1)


def insert_embeddings(embeddings, metaData, vectorId, chunk_text):
    try:
        print("Inserting to pinecone...")
        index.upsert(
            vectors=[
                {
                    'id':vectorId,
                    'values':embeddings,
                     'metadata':{'chunk_text': chunk_text},
                }
            ]
        )
        print("Inserted...")
    except Exception as e:
        print(f"An error occured during insertion: {e}")

async def get_chunk_embeddings():
    chunks = get_chunks()
    count = 1
    all_embeddings = await asyncio.gather(*[async_get_embeddings(chunk) for chunk in chunks])
    return all_embeddings
'''
    for chunk in chunks:
        all_embeddings.append(async_get_embeddings(text=chunk))
        print(f"Requested embeddings for chunk {count}")
        count += 1
    all_embeddings1 = await asyncio.gather(*all_embeddings)
'''
'''
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
'''

async def store_chunk_embeddings():
    chunks = get_chunks()
    all_embeddings = await get_chunk_embeddings()
    count = 1
    tasks = []

    for embeddings in all_embeddings:
        current_chunk = chunks[count-1]
        task = asyncio.to_thread(insert_embeddings, embeddings, f'chunk{count}', f'chunk{count}', current_chunk)
        print(f"Inserted embeddings for chunk {count}")
        count += 1
        tasks.append(task)

    await asyncio.gather(*tasks)
    print("DONE for all chunks.")


asyncio.run(store_chunk_embeddings())