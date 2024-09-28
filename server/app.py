from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from create_script import normalize_text, condense, convertToScript

from transformers import pipeline
import openai
import PyPDF2
import os
import unicodedata
import re

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
	return "hello"

@app.route('/api/create_script', methods=['POST'])
def handle_data():
    if request.method == 'POST':
        data = request.get_json()["text"]
        duration = int (request.get_json()["duration"])
        
        script = create_script(duration, data)

        split_script = script.split(" ");
        res_arr = []
        res_arr_idx = -1
        for i in range(len(split_script)):
            if i % 100 == 0:
                res_arr_idx += 1
                res_arr.append("")

            res_arr[res_arr_idx] = res_arr[res_arr_idx] + " " + split_script[i]
        
        return jsonify({'message': 'Data received', 'text': res_arr})


''' Create Script Methods '''

# Run all create_script methods and return final response
def create_script(maxDuration, text, WPM=160):
    maxWords = maxDuration * WPM
    
    response = convertToScript(text)
    if (len(response) > maxWords):
        response = condense(response, maxWords)
    
    return response

if __name__ == '__main__':
	app.run(debug=True)