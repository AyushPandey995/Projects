import pandas as pd
import EmbeddingModule
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast
import requests

df = pd.read_csv("embeddings.csv")
# print(df)
df["embedding"] = df["embedding"].apply(ast.literal_eval)
Query = input("Ask a qustion- ")
Query_Embedding = EmbeddingModule.create_embedding([Query])[0]
# print(np.vstack(df["embedding"].values))
# print(np.vstack(df["embedding"]).shape)
similarities = cosine_similarity(np.vstack(df["embedding"]), [Query_Embedding]).flatten()
# print(similarities)
top_result = 5
max_similarities_index = similarities.argsort()[::-1][0:top_result]
# print(max_similarities_index)

new_df = df.loc[max_similarities_index]

chunk_data = new_df[
    ["Lecture", "Title", "Start", "End", "Text"]
].to_string(index=False)

prompt = f"""
You are a helpful assistant for a Quantitative Aptitude video playlist.

The user is learning Quantitative Aptitude through a series of videos. 
Below are the details of video chunks available in the playlist.

Each chunk contains:
- Lecture: Lecture 
- Title: Topic/title of the video chunk
- Start: Starting timestamp of the chunk in seconds
- End: Ending timestamp of the chunk in seconds
- Text: Content of the video chunk

VIDEO CHUNK DATA:
{chunk_data}

---------------------------------------------------------------

USER QUESTION:
"{Query}"

---------------------------------------------------------------

TASK:
1. Understand the user's question carefully.
2. Compare the question with the provided video chunk data.
3. Identify the chunk that contains the answer or is most directly relevant to the question.
4. If a relevant chunk is found, tell the user:
   - Lecture 
   - Video/topic title
   - Timestamp where the relevant content starts
   - Timestamp where the relevant content ends
5. Convert the timestamps from seconds into MM:SS format.
6. If multiple chunks are relevant, list the most relevant ones first.
7. Do not make up any lecture, title, timestamp, or information that is not present in the provided data.
8. If none of the provided chunks are relevant to the user's question, reply exactly:
   "No data found for this question."

Keep the answer short and directly useful to the user.
"""

def inference (prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model" : "llama3.2",
        "model" : "deepseek-r1",
        "prompt" : prompt,
        "stream" : False
    })
    response = r.json()["response"]
    return response

print(inference(prompt))
