import os
import sys
from flask import Flask, render_template, send_from_directory
from hava_durumu_app.weather_api import weather_bp

# Klasör yollarını portalın anlayacağı şekilde sabitleyelim
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'hava_durumu_secret_key_2024'

# API'yi kaydet
app.register_blueprint(weather_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

# PWA yolları
@app.route('/manifest.json')
def pwa_manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

@app.route('/sw.js')
def pwa_sw():
    return send_from_directory(app.static_folder, 'sw.js')

if __name__ == '__main__':
    app.run(port=5052)