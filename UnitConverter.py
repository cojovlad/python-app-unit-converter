import os

from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

# AIML API Key and Base URL
api_key = os.getenv("API_KEY")
base_url = 'https://api.aimlapi.com/v1'

# Initialize OpenAI client with AIML API endpoint
api = OpenAI(api_key=api_key, base_url=base_url)

def convert_units(value, from_unit, to_unit):
    completion = api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled in unit conversions."},
            {"role": "user", "content": f"Convert {value} {from_unit} to {to_unit}."}
        ],
        temperature=0.3,
        max_tokens=256,
    )
    return completion.choices[0].message.content.strip()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        value = request.form["value"]
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]
        result = convert_units(value, from_unit, to_unit)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
