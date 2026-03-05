from flask import Flask, render_template
import os

app = Flask(__name__)

# Buraya her yeni uygulamayı ekleyeceğiz
# Örnek: Hava Durumu ve Döviz şimdilik hazır
@app.route('/')
def home():
    return """
    <html>
        <head><title>Articnc Portal</title></head>
        <body style="font-family:sans-serif; text-align:center; padding:50px; background:#f0f2f5;">
            <h1>🚀 Articnc Teknoloji Portalı</h1>
            <div style="display:flex; justify-content:center; gap:20px; margin-top:30px;">
                <a href="/hava" style="padding:20px; background:white; border-radius:15px; text-decoration:none; box-shadow:0 4px 6px rgba(0,0,0,0.1);">🌤️ Hava Durumu</a>
                <a href="/doviz" style="padding:20px; background:white; border-radius:15px; text-decoration:none; box-shadow:0 4px 6px rgba(0,0,0,0.1);">💰 Döviz Kurları</a>
            </div>
        </body>
    </html>
    """

# Gelecekte her uygulamayı bir "Route" (Yol) olarak buraya bağlayacağız.

if __name__ == "__main__":
    app.run(debug=True, port=8080)