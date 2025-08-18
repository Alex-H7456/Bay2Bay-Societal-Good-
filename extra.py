import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


df_reviews = pd.read_parquet("drug_reviews_with_embeddings.parquet")



#encode the embeddings into the embedding space
def get_reviews(df, number: int, query: str):
    embeddings = np.vstack(df["embeddings"].to_numpy()).astype("float32")
    dim = embeddings.shape[1]
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    #embed the query
    query_embedding = model.encode(query, convert_to_tensor=False)
    #format for the search 
    query_vector = np.array([query_embedding], dtype="float32")
    faiss.normalize_L2(query_vector)

    k = number  # Find the top 5 most similar items
    distances, indices = index.search(query_vector, k)

    # Step 7: Print the search results
    print("Top matches for the query:")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. Drug: {df.iloc[idx]['drugName']}, (score={distances[0][i]:.3f}")
        print(df.iloc[idx]["condition"], df.iloc[idx]["review"] )


get_reviews(df_reviews, 2, "need to stop feeling tired")


"""
from groq import Groq

client = Groq()
completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
      {
        "role": "user",
        "content": "DOing a hackathon what would aid the public good using AI"
      }
    ],
    temperature=1,
    max_completion_tokens=400,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

"""