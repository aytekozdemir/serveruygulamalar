"""
Weather API - Hava durumu işlemleri (standalone)
"""
from flask import Blueprint, jsonify, request, session
import requests
from datetime import datetime, timedelta
import sqlite3

# Standalone: login_required is a no-op pass-through decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated

weather_bp = Blueprint('weather_api', __name__)

def check_weather_permission():
    """Kullanıcının weather uygulamasına izni var mı kontrol et"""
    username = session.get('username')
    if not username:
        return True
    
    try:
        conn = sqlite3.connect('chat_database.db')
        cursor = conn.cursor()
        
        # Kullanıcının user_id'sini al
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_result = cursor.fetchone()
        
        if not user_result:
            return True  # Kullanıcı bulunamazsa varsayılan izin ver
            
        user_id = user_result[0]
        
        # Kullanıcının Havadurumu Uygulaması'na iznini kontrol et
        cursor.execute('''
            SELECT is_allowed FROM user_permissions 
            WHERE user_id = ? AND app_name = ?
        ''', (user_id, 'Havadurumu Uygulaması'))
        
        permission_result = cursor.fetchone()
        conn.close()
        
        if permission_result:
            return bool(permission_result[0])
        else:
            # İzin kaydı yoksa varsayılan olarak true döndür
            return True
            
    except Exception as e:
        print(f"❌ Weather permission check error: {e}")
        return True  # Hata durumunda erişime izin ver

# Mock hava durumu verileri
MOCK_WEATHER_DATA = {
    'current': {
        'location': 'Istanbul, Turkey',
        'temperature': 18,
        'description': 'Parçalı bulutlu',
        'humidity': 65,
        'wind_speed': 12,
        'pressure': 1013,
        'feels_like': 20,
        'icon': '02d'
    },
    'forecast': [
        {
            'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'day': 'Yarın',
            'high': 22,
            'low': 15,
            'description': 'Güneşli',
            'icon': '01d'
        },
        {
            'date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'day': 'Öbür gün',
            'high': 19,
            'low': 12,
            'description': 'Yağmurlu',
            'icon': '10d'
        },
        {
            'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'day': '3 gün sonra',
            'high': 24,
            'low': 16,
            'description': 'Kapalı',
            'icon': '04d'
        }
    ]
}

# Türkiye'nin büyük şehirleri
TURKEY_CITIES = {
    'istanbul': {'lat': 41.0082, 'lon': 28.9784, 'name': 'İstanbul'},
    'ankara': {'lat': 39.9334, 'lon': 32.8597, 'name': 'Ankara'},
    'izmir': {'lat': 38.4192, 'lon': 27.1287, 'name': 'İzmir'},
    'bursa': {'lat': 40.1826, 'lon': 29.0665, 'name': 'Bursa'},
    'antalya': {'lat': 36.8969, 'lon': 30.7133, 'name': 'Antalya'},
    'adana': {'lat': 37.0000, 'lon': 35.3213, 'name': 'Adana'},
    'gaziantep': {'lat': 37.0662, 'lon': 37.3833, 'name': 'Gaziantep'},
    'konya': {'lat': 37.8667, 'lon': 32.4833, 'name': 'Konya'},
    'mersin': {'lat': 36.8000, 'lon': 34.6333, 'name': 'Mersin'},
    'diyarbakir': {'lat': 37.9144, 'lon': 40.2306, 'name': 'Diyarbakır'}
}

WEATHER_CODE_MAP = {
    0: 'Açık',
    1: 'Çoğunlukla açık',
    2: 'Parçalı bulutlu',
    3: 'Kapalı',
    45: 'Sisli',
    48: 'Kırağı sisli',
    51: 'Hafif çisenti',
    53: 'Çisenti',
    55: 'Yoğun çisenti',
    56: 'Hafif donan çisenti',
    57: 'Yoğun donan çisenti',
    61: 'Hafif yağmur',
    63: 'Yağmur',
    65: 'Kuvvetli yağmur',
    66: 'Hafif donan yağmur',
    67: 'Kuvvetli donan yağmur',
    71: 'Hafif kar',
    73: 'Kar',
    75: 'Yoğun kar',
    77: 'Kar taneleri',
    80: 'Hafif sağanak',
    81: 'Sağanak',
    82: 'Kuvvetli sağanak',
    85: 'Hafif kar sağanağı',
    86: 'Yoğun kar sağanağı',
    95: 'Gök gürültülü fırtına',
    96: 'Hafif dolulu fırtına',
    99: 'Kuvvetli dolulu fırtına'
}


def get_weather_description(code):
    return WEATHER_CODE_MAP.get(code, 'Bilinmiyor')


def get_weather_icon(code, is_day=True):
    if code == 0:
        return '01d' if is_day else '01n'
    if code in (1, 2):
        return '02d' if is_day else '02n'
    if code in (3, 45, 48):
        return '03d'
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return '10d'
    if code in (71, 73, 75, 77, 85, 86):
        return '13d'
    if code in (95, 96, 99):
        return '11d'
    return '02d'


def resolve_city_coordinates(city):
    city_key = (city or '').strip().lower()
    city_info = TURKEY_CITIES.get(city_key)
    if city_info:
        return city_info['lat'], city_info['lon'], city_info['name']

    try:
        geo_response = requests.get(
            'https://geocoding-api.open-meteo.com/v1/search',
            params={
                'name': city or 'Istanbul',
                'count': 1,
                'language': 'tr',
                'country': 'TR'
            },
            timeout=10
        )
        geo_data = geo_response.json() if geo_response.status_code == 200 else {}
        results = geo_data.get('results') or []
        if results:
            result = results[0]
            return result.get('latitude'), result.get('longitude'), result.get('name', city)
    except Exception:
        pass

    default_city = TURKEY_CITIES['istanbul']
    return default_city['lat'], default_city['lon'], default_city['name']


def build_forecast_days(daily):
    if not daily:
        return MOCK_WEATHER_DATA['forecast']

    dates = daily.get('time') or []
    max_temps = daily.get('temperature_2m_max') or []
    min_temps = daily.get('temperature_2m_min') or []
    codes = daily.get('weather_code') or []

    forecast = []
    for index, date_value in enumerate(dates[:5]):
        if index == 0:
            day_label = 'Bugün'
        elif index == 1:
            day_label = 'Yarın'
        else:
            day_label = f'{index} gün sonra'

        code = int(codes[index]) if index < len(codes) and codes[index] is not None else 2
        forecast.append({
            'date': date_value,
            'day': day_label,
            'high': round(max_temps[index]) if index < len(max_temps) and max_temps[index] is not None else 0,
            'low': round(min_temps[index]) if index < len(min_temps) and min_temps[index] is not None else 0,
            'description': get_weather_description(code),
            'icon': get_weather_icon(code)
        })

    return forecast if forecast else MOCK_WEATHER_DATA['forecast']


def get_weather_data(city=None, lat=None, lon=None):
    """Open-Meteo API'den gerçek hava durumu verisi al"""
    try:
        if lat is not None and lon is not None:
            latitude = float(lat)
            longitude = float(lon)
            location_name = 'Konum'
        else:
            latitude, longitude, resolved_name = resolve_city_coordinates(city or 'istanbul')
            location_name = resolved_name or (city or 'İstanbul')

        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,pressure_msl,wind_speed_10m,weather_code,is_day',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min',
                'forecast_days': 5,
                'timezone': 'auto'
            },
            timeout=15
        )

        if response.status_code != 200:
            return MOCK_WEATHER_DATA

        data = response.json()
        current = data.get('current') or {}
        weather_code = int(current.get('weather_code', 2))
        is_day = bool(current.get('is_day', 1))

        return {
            'current': {
                'location': f"{location_name}, Turkey",
                'temperature': round(float(current.get('temperature_2m', 0))),
                'description': get_weather_description(weather_code),
                'humidity': round(float(current.get('relative_humidity_2m', 0))),
                'wind_speed': round(float(current.get('wind_speed_10m', 0))),
                'pressure': round(float(current.get('pressure_msl', 1013))),
                'feels_like': round(float(current.get('apparent_temperature', current.get('temperature_2m', 0)))),
                'icon': get_weather_icon(weather_code, is_day)
            },
            'forecast': build_forecast_days(data.get('daily'))
        }
            
    except Exception as e:
        print(f"Hava durumu API hatası: {e}")
        return MOCK_WEATHER_DATA

def format_weather_data(current_data, forecast_data=None):
    """API verilerini formatla"""
    try:
        formatted = {
            'current': {
                'location': f"{current_data['name']}, {current_data['sys']['country']}",
                'temperature': round(current_data['main']['temp']),
                'description': current_data['weather'][0]['description'],
                'humidity': current_data['main']['humidity'],
                'wind_speed': round(current_data['wind']['speed'] * 3.6),  # m/s to km/h
                'pressure': current_data['main']['pressure'],
                'feels_like': round(current_data['main']['feels_like']),
                'icon': current_data['weather'][0]['icon']
            },
            'forecast': []
        }
        
        if forecast_data and 'list' in forecast_data:
            # 5 günlük tahmin (günde bir veri)
            daily_forecasts = {}
            for item in forecast_data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'date': date,
                        'high': round(item['main']['temp_max']),
                        'low': round(item['main']['temp_min']),
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon']
                    }
                else:
                    # Günün en yüksek ve en düşük sıcaklıklarını güncelle
                    daily_forecasts[date]['high'] = max(daily_forecasts[date]['high'], round(item['main']['temp_max']))
                    daily_forecasts[date]['low'] = min(daily_forecasts[date]['low'], round(item['main']['temp_min']))
            
            # İlk 5 günü al
            for i, (date, forecast) in enumerate(list(daily_forecasts.items())[:5]):
                if i == 0:
                    forecast['day'] = 'Bugün'
                elif i == 1:
                    forecast['day'] = 'Yarın'
                else:
                    forecast['day'] = f'{i} gün sonra'
                formatted['forecast'].append(forecast)
        else:
            formatted['forecast'] = MOCK_WEATHER_DATA['forecast']
        
        return formatted
        
    except Exception as e:
        print(f"Hava durumu format hatası: {e}")
        return MOCK_WEATHER_DATA

@weather_bp.route('/weather')
@login_required
def get_weather():
    """Hava durumu bilgisini döndür"""
    try:
        # Kullanıcının weather uygulamasına izni var mı kontrol et
        if not check_weather_permission():
            return jsonify({
                'error': 'Permission denied',
                'message': 'Havadurumu uygulamasına erişim izniniz yok',
                'success': False
            }), 403
        
        city = request.args.get('city', 'istanbul')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if lat and lon:
            weather_data = get_weather_data(lat=float(lat), lon=float(lon))
        else:
            weather_data = get_weather_data(city=city)
        
        return jsonify({
            'status': 'success',
            'data': weather_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Hava durumu alınırken hata oluştu: {str(e)}',
            'data': MOCK_WEATHER_DATA
        })

@weather_bp.route('/weather/cities')
@login_required
def get_cities():
    """Türkiye şehirlerini döndür"""
    cities = []
    for key, value in TURKEY_CITIES.items():
        cities.append({
            'id': key,
            'name': value['name'],
            'lat': value['lat'],
            'lon': value['lon']
        })
    
    return jsonify({
        'status': 'success',
        'cities': cities
    })

@weather_bp.route('/weather/current-location')
@login_required
def get_weather_by_location():
    """Koordinatlara göre hava durumu"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({
                'status': 'error',
                'message': 'Konum bilgisi gerekli'
            })
        
        weather_data = get_weather_data(lat=float(lat), lon=float(lon))
        
        return jsonify({
            'status': 'success',
            'data': weather_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Konum tabanlı hava durumu hatası: {str(e)}',
            'data': MOCK_WEATHER_DATA
        })
