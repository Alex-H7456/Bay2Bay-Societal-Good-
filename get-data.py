

#used to clean data for other input 
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
df_real = pd.read_json("hf://datasets/flxclxc/encoded_drug_reviews/encoded_drug_reviews.jsonl", lines=True)

df = df_real.copy(deep=True)


df["search_text"] = (
    "Drug: " + df["drugName"].astype(str) +
    " | Condition: " + df["condition"].astype(str) +
    " | Review: " + df["review"].astype(str)
)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = df['search_text'].tolist()

#get embeddings
new_embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
embeddings = new_embeddings.astype("float32")

df["embeddings"]=embeddings.tolist()
df = df.drop(columns=["encoded"])
print(df.head())

df.to_parquet("drug_reviews_with_embeddings.parquet", index=False)