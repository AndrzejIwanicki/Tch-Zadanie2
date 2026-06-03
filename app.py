import os
from datetime import datetime
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

AUTHOR_NAME = "Andrzej Iwanicki"
PORT = 5000

def log_startup():
    print("-" * 30)
    print(f"DATA URUCHOMIENIA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"AUTOR PROGRAMU:   {AUTHOR_NAME}")
    print(f"PORT TCP:         {PORT}")
    print("-" * 30)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    cities = [
        {"name": "Warszawa", "code": "Warsaw,PL"},
        {"name": "Londyn", "code": "London,GB"},
        {"name": "Nowy Jork", "code": "New York,US"},
        {"name": "Tokio", "code": "Tokyo,JP"}
    ]

    if request.method == 'POST':
        city_code = request.form.get('city')
        API_KEY = "KLUCZ API"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_code}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
            else:
                error = "Nie udało się pobrać danych pogodowych."
        except Exception as e:
            error = f"Błąd połączenia: {e}"

    return render_template('index.html', cities=cities, weather=weather_data, error=error)

if __name__ == '__main__':
    log_startup()
    app.run(host='0.0.0.0', port=PORT)