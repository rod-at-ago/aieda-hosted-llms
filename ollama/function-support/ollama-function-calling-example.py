#!/usr/bin/env python

def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a: The first integer number
    b: The second integer number

  Returns:
    int: The sum of the two numbers
  """
  return a + b

import ollama

response = ollama.chat(
  'llama3.2',
  messages=[{'role': 'user', 'content': 'What is 10 + 10?'}],
  tools=[add_two_numbers], # Actual function reference
)

available_functions = {
  'add_two_numbers': add_two_numbers,
}

for tool in response.message.tool_calls or []:
  function_to_call = available_functions.get(tool.function.name)
  if function_to_call:
    print('Function output:', function_to_call(**tool.function.arguments))
  else:
    print('Function not found:', tool.function.name)


import ollama
import requests

available_functions = {
  'request': requests.request,
}

response = ollama.chat(
  'llama3.2',
  messages=[{
    'role': 'user',
    'content': 'get the ollama.com webpage?',
  }],
  tools=[requests.request], 
)

for tool in response.message.tool_calls or []:
  function_to_call = available_functions.get(tool.function.name)
  if function_to_call == requests.request:
    # Make an HTTP request to the URL specified in the tool call
    resp = function_to_call(
      method=tool.function.arguments.get('method'),
      url=tool.function.arguments.get('url'),
    )
    print(resp.text)
  else:
    print('Function not found:', tool.function.name)

