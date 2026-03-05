from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Akıllı Uygulamalar Portalı</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: sans-serif; text-align: center; padding: 50px; background: #f0f2f5; color: #333; }
                .container { max-width: 800px; margin: auto; }
                .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 30px; }
                .card { padding: 30px; background: white; border-radius: 15px; text-decoration: none; color: #333; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s; display: block; }
                .card:hover { transform: translateY(-5px); background: #eef2ff; }
                .icon { font-size: 40px; margin-bottom: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 AKILLI UYGULAMALAR</h1>
                <p>Tüm dijital araçlarınıza buradan erişebilirsiniz.</p>
                <div class="grid">
                    <a href="/hava" class="card">
                        <div class="icon">🌤️</div>
                        <h3>Hava Durumu</h3>
                    </a>
                </div>
            </div>
        </body>
    </html>
    """

from hava_durumu_app.app import app as hava_app
app.register_blueprint(hava_app, url_prefix='/hava')

if __name__ == "__main__":
    app.run(debug=True, port=8080)