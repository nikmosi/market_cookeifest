import os
from connection import client
from promt import search_query_prompt, product_validation_prompt


model = os.getenv("OLLAMA_MODEL")

def product_validation(productInfo):
  response = client.chat(model=model, messages=[
  {
    'role': 'system',
    'content': search_query_prompt,
  },
  {
    'role': 'user',
    'content': productInfo,
  },
  ])
  return response['message']['content']

def search_alternative(productInfo, alternativeProductInfo):
  response = client.chat(model=model, messages=[
  {
    'role': 'system',
    'content': product_validation_prompt(productInfo),
  },
  {
    'role': 'user',
    'content': alternativeProductInfo,
  },
  ])
  return response['message']['content']


