from transformers import pipeline
from transformers import BartTokenizer
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
    replacements = {
        '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
        '₆': '6', '₇': '7', '₈': '8', '₉': '9', '₀': '0',
        '…': 'and so on', '−': 'minus', '+': 'plus', '=': 'equals',
    }
    
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    
    # Remove any other special characters not replaced above
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!-]', '', text)
    text = text.replace("\n", " ").strip()

    return text

def condense(text, max_words):
    CHAR_PER_WORDS = 4.7
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    normalized_article = normalize_text(text)
    
    max_char = int(max_words * CHAR_PER_WORDS)
    proportion_reduction = max_char / len(text)
    tokenized_text = tokenizer(text)
    
    max_tokens = int(len(tokenized_text['input_ids']) * proportion_reduction)
    
    # print("proportion_reduction")
    # print(proportion_reduction)
    
    # print("tokenized_text")
    # print(tokenized_text)
    
    # print("max_tokens")
    # print(max_tokens)
    # (current) expect / current = expect
    
    WORD_PER_TOKEN = 0.67  # This is a rough average; you may want to adjust it based on your specific data
    token_count = int(max_char / WORD_PER_TOKEN)  # Convert words to tokens

    # Define max and min lengths based on token counts
    max_length = min(token_count, 1024)  # Set to max token limit of the model
    min_length = int(max_length * 0.4)  # Minimum is 40% of max_length


    MAX_INPUT_LENGTH = 1024
    chunks = [normalized_article[i:i + MAX_INPUT_LENGTH] for i in range(0, len(normalized_article), MAX_INPUT_LENGTH)]
    
    summaries = []
    gpt_summaries = []
    for chunk in chunks:
        try:
            # print("chunk pre-GPT")
            # print(chunk)
            
            tokenized_text = tokenizer(chunk)
            max_tokens = int(len(tokenized_text['input_ids']) * proportion_reduction)
            # print("max_tokens")
            # print(max_tokens)
            
            chunk_summary = summarizer(chunk, max_length=max_tokens, min_length=int(0.4 * max_tokens), do_sample=False)
            # print("CONDENSED")
            # print(chunk_summary[0]['summary_text'])
            
            spell_checked_chunk = gpt_call("You are an assistant that completes spell-checking.", "Write out the gramatically correct form of: " + chunk_summary[0]['summary_text'] + ". Don't state whether changes are needed or not.")
            summaries.append(spell_checked_chunk)
            # print("spell_checked_chunk")
            # print(spell_checked_chunk)
            
        except Exception as e:
            print(f"An error occurred while summarizing chunk: {e}")
    
    condensed_summary = " ".join(summaries)
    
    # print("condensed_summary")
    # print(condensed_summary)
    
    return condensed_summary

def gpt_call(system_prompt, user_prompt):
    openai.api_key = api_key
    
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    output = response['choices'][0]['message']['content']
    
    return output

def convertToScript(text):
    openai.api_key = api_key
    max_length = len(text.split())
    max_tokens = 1000
    chunks = [text[i:i + max_tokens] for i in range(0, len(text), max_tokens)]

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

def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text