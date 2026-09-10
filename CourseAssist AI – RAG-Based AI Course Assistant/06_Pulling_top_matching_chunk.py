import pandas as pd
import EmbeddingModule
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast

df = pd.read_csv("embeddings.csv")
# print(df)
df["embedding"] = df["embedding"].apply(ast.literal_eval)
Query = input("Ask a qustion- ")
Query_Embedding = EmbeddingModule.create_embedding([Query])[0]
# print(np.vstack(df["embedding"].values))
# print(np.vstack(df["embedding"]).shape)
similarities = cosine_similarity(np.vstack(df["embedding"]), [Query_Embedding]).flatten()
print(similarities)
max_similarities_index = similarities.argsort()[::-1][:3]
print(max_similarities_index)

new_df = df.loc[max_similarities_index]
# print(new_df)
# print(new_df[["Lecture", "Title", "Text"]])

for index, item in new_df.iterrows():
    print(index, item["Lecture"], item["Title"], item["Text"] )


 






