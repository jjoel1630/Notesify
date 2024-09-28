from transformers import pipeline

import openai
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN-API-KEY")

# BART Transformer
# IF needed, summarize text to get it below limit
def summarize(text, max_words):
    # Example summarization using BART or similar transformer if needed
    pass

# GPT
# Convert note text to lecture-style script
def convertToScript(text):
    openai.api_key = api_key
    
    # Calculate the maximum output length
    max_length = len(text.split())
    
    max_tokens = 1000
    chunks = [text[i:i+max_tokens] for i in range(0, len(text), max_tokens)]
    
    script = []
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that converts notes to a script."},
                {"role": "user", "content": f"Please reword the following text to be a short script that is less than the length of the input: {chunk}"}
            ]
        )
        # Check length of the response and trim if necessary
        output = response['choices'][0]['message']['content']
        if len(output.split()) > max_length:
            output = " ".join(output.split()[:max_length])  # Trim to max length
        script.append(output)
    
    # Combine the summaries if there are multiple chunks
    full_script = " ".join(script)
    return full_script

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()  # Read the entire content of the file
    return text

if __name__ == "__main__":
    file_path = "/Users/anujnaik/Desktop/HackGT/hackgt-project/server/notes_example.txt"
    openai.api_key = api_key
    
    text = read_text(file_path)
    response = convertToScript(text)
    
    print(response)