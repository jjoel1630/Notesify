from flask import Flask, render_template, request, url_for, redirect, session

from transformers import pipeline
import openai
import PyPDF2
import os
import unicodedata
import re

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN-API-KEY")

app = Flask(__name__)


@app.route('/')
def index():
	return "hello"

''' Create Script Methods '''
# Helper method to remove special characteres
def normalize_text(text):
    text = unicodedata.normalize('NFKD', text)

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
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!-]', '', text)

    return text

# Condense text to max_words words with BART if necessary
def condense(text, max_words):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    normalized_article = normalize_text(text)

    WORD_PER_TOKEN = 0.75
    TARGET_WORDS = max_words

    max_tokens = int(TARGET_WORDS / WORD_PER_TOKEN)
    min_tokens = int(0.8 * max_tokens)

    summary = summarizer(normalized_article, max_length=max_tokens, min_length=min_tokens, do_sample=False)
    
    return summary[0]['summary_text'] if summary else text

# Use GPT to create a script from raw text
def convertToScript(text):
    openai.api_key = api_key
    
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
        output = response['choices'][0]['message']['content']
        if len(output.split()) > max_length:
            output = " ".join(output.split()[:max_length])  # Trim to max length
        script.append(output)
    
    full_script = " ".join(script)
    return full_script

# Run all create_script methods and return final response
def create_script(maxDuration, text, WPM=160):
    maxWords = maxDuration * WPM
    
    response = convertToScript(text)
    if (len(response) > maxWords):
        response = condense(response, maxWords)
    
    return response

if __name__ == '__main__':
	app.run(debug=True)