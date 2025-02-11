curl http://localhost:11434/api/chat -d '{
  "model": "llama3:70b",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ],
  "stream": false
}'
