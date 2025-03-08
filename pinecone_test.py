from pinecone import Pinecone, ServerlessSpec
from key import pineconeKey
from embeddings import get_embeddings

text1 = """
Hey Mister tambourine man, play a song for me, I'm not sleepy and there ain't no place I'm going to.
Hey Mr. tambourine man, play a song for me, in the jingle jangle morning, i'll come follwing you.
Take me for a magic in upon your swirlin's ship, all my senses have been stripped, and my hands can't feel the grip, and my toes too numb to step,
Wait only for my boots hills to be wanderin.
I'm ready to go anywhere I'm ready for to fade, unto my own parade, cast your dancing spell my way, i promise to go under it.
Hey mr tambourine man, play a song for me, i'm not sleepy and there ain't no place i'm going to.
hey mr tambourine man, play a song for me, in the jingle jangle morning, i'll come followin you.
"""
pc = Pinecone(api_key=pineconeKey)

embeddings = get_embeddings(text=text1)

environment = "us-east-1-aws"
index_list = pc.list_indexes()

index_name = "story-index"

index = pc.Index(index_name)

vector_id = "text1"  #setting a unique vector id for this vector in vectorDB

def insert_embeddings(embeddings, metaData, vectorId):
    try:
        index.upsert(
            vectors=[
                {
                    'id':vector_id,
                    'values':embeddings,
                    'metadata':{'about': metaData}
                }
            ]
        )
        print("Inserted Successfully")
    except Exception as e:
        print(f"An error occured during insertion: {e}")


insert_embeddings(embeddings=embeddings, metaData="hey mr tambourine man.", vectorId=vector_id)