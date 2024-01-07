import os
from flask import Flask, render_template, request, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from openai import OpenAI
from dotenv import load_dotenv
import secrets

from utils import resize_image

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
google_bp = make_google_blueprint(client_id=os.environ.get("client_id"),
                                  client_secret=os.environ.get("client_secret"),
                                  redirect_to='google_login')


app = Flask(__name__)

app.register_blueprint(google_bp, url_prefix='/index')
app.secret_key = secrets.token_hex(16)

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/')
def index():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/plus/v1/people/me')
    assert resp.ok, resp.text
    # Here, you can use the information from `resp.json()` to create or authenticate the user
    user_info = resp.json()
    # Implement your user handling logic (create user, log in, etc.)
    return render_template('index.html', user_info=user_info)


@app.route('/login/google/authorized')
def google_callback():
    # This route is automatically called after a successful Google Sign-In
    return redirect(url_for('index'))


@app.route('/generate_logo', methods=['POST'])
def generate_logo():

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

@app.route('/login')
def login():
    return redirect(url_for('google.login'))



if __name__ == '__main__':
    app.run(debug=True)
