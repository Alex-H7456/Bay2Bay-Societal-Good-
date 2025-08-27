import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from drug_call import Drug
from groq import Groq
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"



class SearchGo:
  #encode the embeddings into the embedding space
  def __init__(self, response: str, num_entries: int, database, resolution: float = 0.28):
    self.response = response
    self.num = num_entries
    self.resolution = resolution
    self.database = database
    self.output ={
       "reviews" : {
          "ID": [],
          "DrugName": [],
          "score": [],
          "condition": [],
          "review": []

       },
       "AI": {
          "long": "",
          "truncated": ""
       }
    }
    self.main()

  def main(self):
    print("database done")
    top_drug = self.get_reviews(self.database, self.num, self.response)
    print("embeddings done")
    model = Drug()
    report3 = model.get_drug_FDA(top_drug, 1, "label") #1 refers to number of queries this is enough
    print("FDA done")
    if report3 == None:
      print("Drug not in FDA database or no drug found")
      self.output["AI"]["truncated"] = "Drug not in FDA database or no drug found"
    
    else:
      report3 = model.filter_events_FDA(report3)
      report3 = model.summarise_drug_info(report3)
      self.prompt_AI(report3)
    print("Grok")



  def get_reviews(self, df, number: int, query: str):
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
        self.output["reviews"]["ID"].append(df.iloc[idx]["patient_id"])
        self.output["reviews"]["DrugName"].append(df.iloc[idx]['drugName'])
        self.output["reviews"]["score"].append(distances[0][i])
        self.output["reviews"]["condition"].append(df.iloc[idx]['condition'])
        self.output["reviews"]["review"].append(df.iloc[idx]['review'])

      if self.output["reviews"]["score"][0] < self.resolution:
          return None
      else:
        return df.iloc[indices[0][0]]["drugName"]


  def prompt_AI(self, prompt: str):

    client = Groq()
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
          {
            "role": "user",
            "content": f"Write a review of the top search response drug only drawing on information in this response by the FDA {prompt}. Remove excessive formatting. "
          }
        ],
        temperature=1,
        max_completion_tokens=1000,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )

    AI_text =""

    for chunk in completion:
        piece= chunk.choices[0].delta.content or ""
        AI_text += piece

    self.output["AI"]["long"] =AI_text


    shorter = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
          {
            "role": "user",
            "content": f" truncate {AI_text} into a summary of between 90 and 150 words and add headings for clarity. Do not add any information in creating the review "
          }
        ],
        temperature=1,
        max_completion_tokens=1000,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )

    AI_text_short =""
    for chunk in shorter:
          nibble= chunk.choices[0].delta.content or ""
          AI_text_short += nibble

    self.output["AI"]["truncated"] = AI_text_short






if __name__ == "__main__":

  df_reviews = pd.read_parquet("drug_reviews_with_embeddings.parquet")  
  test = SearchGo("feeling depressed", 3,df_reviews, 0.25)
  print(test.output["AI"]["truncated"])



