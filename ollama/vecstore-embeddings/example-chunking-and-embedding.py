#!/usr/bin/env python

import yaml
import os
import argparse
import pprint
from pprint import PrettyPrinter
pp = PrettyPrinter(width=200)

import faiss
import numpy as np
from ollama import embed

def chunk_text(text, chunk_size=512):
    """Splits text into overlapping chunks of a given token size."""
    words = text.split()  # Basic tokenization
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Load the file
# with open("cz_core_splat.sv", "r", encoding="utf-8") as f:
with open("cuzco-microarchitecture-specification-v0.2.pdf.txt", "r", encoding="utf-8") as f:
    file_content = f.read()

# Chunk the document
chunks = chunk_text(file_content)

# Generate embeddings for each chunk
MODEL_NAME = 'mxbai-embed-large'
chunk_embeddings = [embed(model=MODEL_NAME, input=chunk)['embeddings'] for chunk in chunks]

# Ensure the embeddings are correctly shaped as (num_chunks, embedding_dim)
chunk_embeddings_np = np.array(chunk_embeddings, dtype=np.float32)

# Check actual embedding dimensions
num_chunks, embedding_dim = chunk_embeddings_np.shape

# Initialize FAISS with correct dimensions
index = faiss.IndexFlatL2(embedding_dim)

# Add embeddings to FAISS
index.add(chunk_embeddings_np)

# Store chunk references
chunk_map = {i: chunk for i, chunk in enumerate(chunks)}

print("Exiting before the query")
exit()

# Function to retrieve relevant chunk for a query
def retrieve_relevant_chunk(query, top_k=1):
    query_embedding = np.array([embed(model=MODEL_NAME, input=query)['embeddings']], dtype=np.float32)
    distances, indices = index.search(query_embedding, top_k)
    return [chunk_map[i] for i in indices[0]]

def query():
    pass # add below to this
# Test retrieval
query = "What is the main topic of the document?"
retrieved_chunks = retrieve_relevant_chunk(query)

print("Top Relevant Chunks:", retrieved_chunks)

def main():

    parser = argparse.ArgumentParser(description="Template python code demonstrating argparse")
    parser.add_argument("argument", help="Required argument")
    args = parser.parse_args()

if __name__ == "__main__":
    main()

