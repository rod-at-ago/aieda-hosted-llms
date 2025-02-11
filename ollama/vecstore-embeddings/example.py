#!/usr/bin/env python

from ollama import embed

with open('cz_core_splat.sv') as f:
    data = f.read()

print(f"Read {len(data)} bytes")

response = embed(
    model='mxbai-embed-large',
    input=data
#   input='Your text here'
)

embeddings = response['embeddings']
