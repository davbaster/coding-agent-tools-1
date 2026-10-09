import os

def read_file(filepath: str) -> str:
    try:
        if filepath == 'uv.lock':
            return "you're not allowed to read this file"

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: file '{filepath}' not found."