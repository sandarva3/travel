import os
from vertexai.language_models import TextEmbeddingModel
import vertexai
from key import projectid, vertex_ai_service_key_path
import asyncio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = vertex_ai_service_key_path


PROJECT_ID = projectid
LOCATION = "us-central1"   # Common region
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Loading the model
model = TextEmbeddingModel.from_pretrained("text-embedding-005")

# text input
#text = "This is a sample text to embed.This is a sample text to embed.This is a sample text to embedThis is a sample text to embed. """


async def async_get_embeddings(text):
    try:
        print("Sending the text for embeddings...")
        embeddings = await asyncio.to_thread(lambda: model.get_embeddings([text])[0].values)
        print("Got embeddings...")
        return embeddings
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_embeddings(text):
    try:
        print("Sending the text for embeddings...")
        embeddings = model.get_embeddings([text])[0].values
        print("Got embeddings...")
        return embeddings
    except Exception as e:
        print(f"Error: {e}")
        return None