#!/usr/bin/env python

def add(a, b):
    return a + b

# Simple dispatcher example
def execute_tool(tool_function, *args, **kwargs):
    try:
        return tool_function(*args, **kwargs)
    except Exception as e:
        return f"An error occurred: {str(e)}"

tool_mapping = {
    "add": add,
    # Add more tools here
}

# Sample usage:
result = execute_tool(tool_mapping["add"], 5, 3)
print(f"Result: {result}")
