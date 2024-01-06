import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_logo', methods=['POST'])
def generate_logo():

    brand_description = request.form['brand_description']
    selected_style = request.form['style']
    selected_type = request.form['type']
    selected_technique = request.form['technique']

    style_mapping = {
        'abstract_expressionism': 'Abstract Expressionism',
        'crystal_cubism': 'Crystal Cubism',
        'pop_art': 'Pop Art',
        'pablo_picasso': 'Pablo Picasso',
        'black_and_white': 'Black and White',
        'paul_rand': 'Paul Rand',
        'piet_mondrian': 'Piet Mondrian'
    }

    type_mapping = {
        'logo_mascot': 'Logo Mascot',
        'lettermark': 'Lettermark',
        'emblem': 'Emblem'
    }

    technique_mapping = {
        'outline': 'Outline',
        'gradient': 'Gradient',
        'screen_print': 'Screen-print'
    }

    selected_style_name = style_mapping.get(selected_style, 'Custom Style')
    selected_type_name = type_mapping.get(selected_type, 'Custom Type')
    selected_technique_name = technique_mapping.get(selected_technique, 'Custom Technique')

    prompt = f"A simple logo of a {brand_description}, {selected_type_name}, {selected_style_name}, {selected_technique_name}, simple, vector. Do not include any letters on the generated image."
    response = client.images.generate(
        model="dall-e-3",  # dall-e-3 for HQ
        prompt=prompt,
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    return render_template('result.html', image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)