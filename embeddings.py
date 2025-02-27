from google import generativeai as genai
from key import googleKey, credentialPath
from story import get_chunks
from google.cloud import aiplatform


aiplatform.init(credentials_path=credentialPath)
genai.configure(api_key=googleKey)

def get_embedding(text):
    print("sending request..")
    result = genai.embed_content(
        model="models/text-embedding-005",
        content=text,
        task_type="RETRIEVAL_DOCUMENT",
        title="Driver's License",
        output_dimensionality=768,
    )
    print("got response.")
    return result["embedding"]

models = genai.list_models()  # Lowercase "list"
print(models)

chunk1 = get_chunks()[0]
embed1 = get_embedding(chunk1)
print("embed1:")
print(embed1)