import requests

# r = requests.post("http://localhost:11434/api/embeddings", json={
#     "model":"bge-m3",
#     "prompt":"Ayush is a good boy" 
# })
# embedding = r.json()["embedding"]

# print(embedding[0:6])

#Now create this as a function
#There is some difference in this code as we can pass an array of texts as input.
def create_embedding (text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model":"bge-m3",
        "input": text_list
    })
    embedding = r.json()["embeddings"]

    return embedding

embedding_result = create_embedding(["Ayush is a good boy", "Ayush is an All rounder"])
print(embedding_result)

