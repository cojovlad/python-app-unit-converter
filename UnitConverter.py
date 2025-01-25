import openai
from flask import Flask, render_template, request

# Set up Flask
app = Flask(__name__)

# OpenAI API key
#openai.api_key = ''  # Replace with your actual API key

# Function to call OpenAI API to process the unit conversion request
def convert_units(value, from_unit, to_unit):
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Free-tier model, replace with your choice
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Convert {value} {from_unit} to {to_unit}."}
        ]
    )
    return completion['choices'][0]['message']['content'].strip()

# Route for handling form submission
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        value = request.form["value"]
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]

        # Call the OpenAI API for conversion
        result = convert_units(value, from_unit, to_unit)

    return render_template("index.html", result=result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
