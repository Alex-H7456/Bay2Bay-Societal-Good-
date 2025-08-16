from transformers import pipeline
#pipeline just does everything for us, so we don't have to write the code ourselves
#can use langchain to wrap everythign together
"""
model = pipeline(task ="summarization", model="facebook/bart-large-cnn")

response = model("the big dog jumped over the fence and ran away with the cat and hare who jumped over the fence")

print(response)

is this how the editing works????
"""
import os

hf_cache = os.getenv("HF_HOME", os.path.expanduser("~/.cache/huggingface"))
print(hf_cache)
