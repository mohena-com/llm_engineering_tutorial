# imports

import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display


# Constants
OLLAMA_URL = "http://localhost:11434"
OLLAMA_API = f"{OLLAMA_URL}/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

# Create a messages list using the same format that we used for OpenAI

messages = [
    {"role": "user", "content": "Describe some of the business applications of Generative AI"}
]

payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

# If this doesn't work for any reason, try the 2 versions in the following cells
# And double check the instructions in the 'Recap on installation of Ollama' at the top of this lab
# And if none of that works - contact me!

# !ollama pull llama3.2

response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
print(f"0. {MODEL} -> {response.json()['message']['content']}")

import ollama

response = ollama.chat(model=MODEL, messages=messages)
print(f"1. {MODEL} -> {response['message']['content']}")

# There's actually an alternative approach that some people might prefer
# You can use the OpenAI client python library to call Ollama:

from openai import OpenAI
ollama_via_openai = OpenAI(base_url=f'{OLLAMA_URL}/v1', api_key='ollama')

response = ollama_via_openai.chat.completions.create(
    model=MODEL,
    messages=messages
)

print(f"{MODEL} -> {response.choices[0].message.content}")
# This may take a few minutes to run! You should then see a fascinating "thinking" trace inside <think> tags, followed by some decent definitions
# !ollama pull deepseek-r1:1.5b
MODEL = "deepseek-r1:1.5b"

response = ollama_via_openai.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Please give definitions of some core concepts behind LLMs: a neural network, attention and the transformer"}]
)

print(f"2. {MODEL} -> {response.choices[0].message.content}")