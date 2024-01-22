import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import secrets
import google.cloud.logging
from google.cloud.logging import DESCENDING

from utils import resize_image

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

client_logs = google.cloud.logging.Client()
client_logs.get_default_handler()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def landing():
    return render_template('index.html')

@app.route('/generate_logo', methods=['POST'])
def generate_logo():

    try:
        brand_description = request.form['brand_description']
        selected_style = request.form['style']
        selected_type = request.form['type']
        selected_technique = request.form['technique']
        selected_color_scheme = request.form['color_scheme']
        selected_shape = request.form['shape']
        selected_additional_style = request.form['additional_style']

        style_mapping = {
            'simple':'Simple',
            'abstract_expressionism': 'Abstract Expressionism',
            'crystal_cubism': 'Crystal Cubism',
            'pop_art': 'Pop Art',
            'pablo_picasso': 'Pablo Picasso',
            'black_and_white': 'Black and White',
            'paul_rand': 'Paul Rand',
            'piet_mondrian': 'Piet Mondrian'
        }

        type_mapping = {
            'logo_mascot': 'Mascot',
            'lettermark': 'Lettermark',
            'emblem': 'Emblem'
        }

        technique_mapping = {
            'outline': 'Outline',
            'gradient': 'Gradient',
            'screen_print': 'Screen-print'
        }

        color_scheme_mapping = {
            'monochromatic': 'Monochromatic',
            'analogous': 'Analogous',
            'complementary': 'Complementary'
        }

        shape_mapping = {
            'geometric': 'Geometric',
            'organic': 'Organic'
        }

        additional_style_mapping = {
            'minimalist': 'Minimalist',
            'retro': 'Retro',
            'vintage': 'Vintage'
        }

        selected_style_name = style_mapping.get(selected_style, 'Custom Style')
        selected_type_name = type_mapping.get(selected_type, 'Custom Type')
        selected_technique_name = technique_mapping.get(selected_technique, 'Custom Technique')
        selected_color_scheme_name = color_scheme_mapping.get(selected_color_scheme, 'Custom Color Scheme')
        selected_shape_name = shape_mapping.get(selected_shape, 'Custom Shape')
        selected_additional_style_name = additional_style_mapping.get(selected_additional_style, 'Custom Additional Style')

        prompt = f"A {selected_type_name} logo for {brand_description} with the following characteristics: " \
                f"Style: {selected_style_name}, Technique: {selected_technique_name}, " \
                f"Color Scheme: {selected_color_scheme_name}, Shape: {selected_shape_name}, " \
                f"Additional Style: {selected_additional_style_name}. " \
                f"Do not include any letters on the generated image."

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        resized_image = resize_image(image_url, target_size=(728, 728))

        return render_template('result.html', image_url=resized_image)
    
    except Exception as e:
        client_logs.setup_logging(f'Occured: {e}',log_level='INFO')
        raise

if __name__ == '__main__':
    app.run(debug=True)