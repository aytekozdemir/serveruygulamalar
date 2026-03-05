from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from hava_durumu_app.app import app as hava_app

# Ana portal uygulaması
portal = Flask(__name__)

@portal.route('/')
def home():
    return """
    <html>
        <head><title>Akilli Uygulamalar</title></head>
        <body style="font-family:sans-serif; text-align:center; padding:50px;">
            <h1>🚀 AKILLI UYGULAMALAR PORTALI</h1>
            <a href="/hava/" style="padding:20px; background:#007bff; color:white; text-decoration:none; border-radius:10px;">☀️ Hava Durumu Uygulamasını Aç</a>
        </body>
    </html>
    """

# İki uygulamayı birleştiriyoruz:
# Ana site / (portal) olacak, /hava ise hava_app olacak.
app = DispatcherMiddleware(portal, {
    '/hava': hava_app
})

# Not: Gunicorn bu 'app' değişkenini görecek ve çalıştıracak.