from flask import Blueprint, jsonify, request

# app.py'nin aradığı weather_bp değişkeni (Blueprint) burada tanımlanıyor
weather_bp = Blueprint('weather_api', __name__)

@weather_bp.route('/durum', methods=['GET'])
def hava_durumu_getir():
    # Frontend'den (HTML'den) gelen şehir bilgisini alıyoruz
    sehir = request.args.get('sehir', 'İstanbul')
    
    # Sitenin çökmemesi ve veriyi hemen göstermesi için geçici örnek veri:
    ornek_veri = {
        "sehir": sehir.capitalize(),
        "sicaklik": 22,
        "durum": "Güneşli",
        "mesaj": "Veri başarıyla çekildi."
    }
    
    return jsonify(ornek_veri)