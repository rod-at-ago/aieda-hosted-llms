#!/usr/bin/env python

import faiss
import numpy as np
from ollama import embed, generate

#
# Read document to be submitted to embedding
#
with open('cz_core_splat.sv') as f:
    data = f.read()

print(f"Read {len(data)} bytes")

#
# Define the embedding model
#
MODEL_NAME = 'mxbai-embed-large'

# Sample data to embed
documents = [
    "Ollama provides an easy way to generate embeddings.",
    "FAISS is a library for efficient similarity search of high-dimensional vectors.",
    "Llama 3.3 can be used for question-answering tasks when combined with embeddings.",
]

# Generate embeddings for the documents
doc_embeddings = [embed(model=MODEL_NAME, input=doc)['embedding'] for doc in documents]

# Convert embeddings to a NumPy array
embedding_dim = len(doc_embeddings[0])  # Determine embedding size
index = faiss.IndexFlatL2(embedding_dim)  # Create FAISS index
index.add(np.array(doc_embeddings, dtype=np.float32))  # Add vectors to FAISS

# Function to retrieve the most relevant document
def retrieve_relevant_doc(query, top_k=1):
    query_embedding = np.array([embed(model=MODEL_NAME, input=query)['embedding']], dtype=np.float32)
    distances, indices = index.search(query_embedding, top_k)
    return [documents[i] for i in indices[0]]

# Function to generate an answer using Llama 3.3
def ask_llama3(query):
    retrieved_docs = retrieve_relevant_doc(query)
    context = "\n".join(retrieved_docs)
    
    response = generate(
        model="llama3",
        prompt=f"Context: {context}\n\nQuestion: {query}\nAnswer:",
    )
    
    return response['response']

# Example question
question = "How does FAISS help with embeddings?"
answer = ask_llama3(question)

print("Q:", question)
print("A:", answer)

