from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from hava_durumu_app.app import app as hava_app

# Ana portal uygulaması
portal = Flask(__name__)

@portal.route('/')
def home():
    return """
    <html>
        <head>
            <title>Akilli Uygulamalar</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: sans-serif; text-align: center; padding: 50px; background: #f0f2f5; color: #333; }
                .container { max-width: 600px; margin: auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
                h1 { color: #1a73e8; margin-bottom: 30px; }
                .btn { display: inline-block; padding: 20px 40px; background: #1a73e8; color: white; text-decoration: none; border-radius: 12px; font-weight: bold; transition: 0.3s; }
                .btn:hover { background: #1557b0; transform: scale(1.05); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 AKILLI UYGULAMALAR PORTALI</h1>
                <p>Dijital araçlarınıza tek bir noktadan erişin.</p>
                <br>
                <a href="/hava/" class="btn">☀️ Hava Durumu Uygulamasını Aç</a>
            </div>
        </body>
    </html>
    """

# İki uygulamayı köprü (Middleware) ile birleştiriyoruz
# ÖNEMLİ: Gunicorn bu 'app' değişkenini çalıştıracak
app = DispatcherMiddleware(portal, {
    '/hava': hava_app
})