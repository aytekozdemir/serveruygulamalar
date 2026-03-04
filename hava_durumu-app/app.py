import os
import sys

# UTF-8 encoding fix
os.environ['PYTHONIOENCODING'] = 'utf-8'
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Ensure working directory is the app's own folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, send_from_directory
from weather_api import weather_bp

app = Flask(__name__, template_folder='templates')
app.secret_key = 'hava_durumu_secret_key_2024'

# Register weather blueprint at /api prefix
app.register_blueprint(weather_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')


# ── PWA ──────────────────────────────────────────
@app.route('/manifest.json')
def pwa_manifest():
    return send_from_directory(app.static_folder, 'manifest.json',
                               mimetype='application/manifest+json')

@app.route('/sw.js')
def pwa_sw():
    resp = send_from_directory(app.static_folder, 'sw.js',
                               mimetype='application/javascript')
    resp.headers['Service-Worker-Allowed'] = '/'
    return resp
# ─────────────────────────────────────────────────

if __name__ == '__main__':
    print('==> Hava Durumu başlatılıyor: http://localhost:5052')
    app.run(host='0.0.0.0', port=5052, debug=True)
