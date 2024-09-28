from transformers import pipeline

import openai
import os
import unicodedata
import re

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

def normalize_text(text):
    # Normalize Unicode characters to their closest ASCII representation
    text = unicodedata.normalize('NFKD', text)

    # Replace problematic characters
    replacements = {
        '₁': '1',
        '₂': '2',
        '₃': '3',
        '₄': '4',
        '₅': '5',
        '₆': '6',
        '₇': '7',
        '₈': '8',
        '₉': '9',
        '₀': '0',
        '…': 'and so on',
        '−': 'minus',
        '+': 'plus',
        '=': 'equals',
        # Add more as necessary
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    # Remove any other special characters not replaced above
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!-]', '', text)

    return text

# BART Transformer
# IF needed, summarize text to get it below limit
# BART Transformer
def condense(text, max_words):
    # Example summarization using BART or similar transformer if needed
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Normalize the input text
    normalized_article = normalize_text(text)

    # Token estimates
    WORD_PER_TOKEN = 0.75
    TARGET_WORDS = max_words  # Target length in words

    # Set lengths in tokens (closer approximation)
    max_tokens = int(TARGET_WORDS / WORD_PER_TOKEN)
    min_tokens = int(0.8 * max_tokens)  # You can make it more flexible by setting a range

    # Call the summarizer with normalized text
    summary = summarizer(normalized_article, max_length=max_tokens, min_length=min_tokens, do_sample=False)
    
    # Summarizer returns a list of dicts, extract the actual text
    return summary[0]['summary_text'] if summary else text  # In case summarizer returns nothing


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
                {"role": "user", "content": f"Reword the following text to be a short script that is less than the length of the input, and replace special characters with English equivalent: {chunk}"}
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
    current_directory = os.getcwd()  # Get the current working directory
    file_name = "notes_example.txt"  # The name of the file
    file_path = os.path.join(current_directory, "server", file_name)  # Construct the absolute path

    openai.api_key = api_key
    
    maxDuration = 3 # minutes
    WPM = 160
    maxWords = maxDuration * WPM
    
    text = read_text(file_path)
    
    response = convertToScript(text)
    if (len(response) > maxWords):
        print("condensing text now")
        print("ORIGINAL INPUT\n" + response + "\n\n")
        response = condense(response, maxWords)
        print("\n\nALTERED OUTPUT\n\n")
    
    print(response)