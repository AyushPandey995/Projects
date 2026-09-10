import requests
def create_embedding (text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model":"bge-m3",
        "input": text_list
    })
    embedding = r.json()["embeddings"]

    return embedding

