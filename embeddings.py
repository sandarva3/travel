from key import googleKey, credentialPath, projectid
from story import get_chunks
from google.cloud import aiplatform
#from google.cloud.aiplatform import TextEmbeddingModel


project = projectid
location = "us-central1"
#aiplatform.init(project=project, location=location, credentials_path=credentialPath)
#aiplatform.init(project=project, location=location, credentials_path=credentialPath)

def get_embedding(text):
    print("sending request..")
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-005")
    embeddings = model.get_embeddings([text], task_type="RETRIEVAL_DOCUMENT")
    print("got response.")
    return embeddings[0].values



# chunk1 = get_chunks()[0]
# embed1 = get_embedding(chunk1)
# print("embed1:")
# print(embed1)

print("MODEL:")
print(dir(aiplatform    ))