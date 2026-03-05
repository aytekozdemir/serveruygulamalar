from flask import Flask, render_template
import os

# Uygulamaları içeri aktarıyoruz
# (Klasör isimlerinizin tam olarak böyle olduğundan emin olun)
from hava_durumu_app.app import app as hava_app
from doviz_app.app import app as doviz_app

app = Flask(__name__)

# Ana sayfa: Tüm uygulamaların listelendiği şık bir menü
@app.route('/')
def index():
    return """
    <h1>Articnc Teknoloji Portalı</h1>
    <ul>
        <li><a href="/hava">Hava Durumu</a></li>
        <li><a href="/doviz">Döviz Kurları</a></li>
    </ul>
    """

# Uygulamaları alt yollara bağlıyoruz
app.register_blueprint(hava_app, url_prefix='/hava')
app.register_blueprint(doviz_app, url_prefix='/doviz')

if __name__ == "__main__":
    app.run(debug=True, port=8000)