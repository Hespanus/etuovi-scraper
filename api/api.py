from flask import Flask, jsonify, request, Response
import requests
from flask_cors import cross_origin # Tuodaan cross_origin-dekorointi
from dotenv import load_dotenv
import os

# Lataa ympäristömuuttujat .env-tiedostosta
load_dotenv()

# Haetaan scraper-palvelun osoite ympäristömuuttujasta
SCRAPER_SERVICE_URL = "http://scraper-service:5001"

app = Flask(__name__)
# POISTETTU: Globaali CORS-tuki, koska käytämme nyt reittikohtaista dekorointia.
# CORS(app)

# Tervehdys-päätepiste (voit tarkistaa, että API on käynnissä)
@app.route('/')
def home():
    return "API-palvelin käynnissä!"

# Scraperin käynnistys-päätepiste
# LISÄTTY: @cross_origin() dekorointi, joka varmistaa CORS-pyyntöjen onnistumisen.
@app.route('/trigger-scraper', methods=['POST'])
@cross_origin()
def trigger_scraper():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL-osoite puuttuu.'}), 400

    try:
        # Välitetään pyyntö scraper-palvelulle
        response = requests.post(f'{SCRAPER_SERVICE_URL}/run', json={'url': url}, stream=True)
        response.raise_for_status()

        # Palautetaan suoraan scraperin vastaus
        return Response(response.content, status=response.status_code, mimetype=response.headers['Content-Type'])
    
    except requests.exceptions.RequestException as e:
        print(f"Virhe pyynnössä scraperiin: {e}")
        return jsonify({'error': f'Virhe pyydettäessä scraperia: {e}'}), 500

# POISTETTU: after_request-funktio, joka ei toiminut odotetusti
# @app.after_request
# def add_cors_headers(response):
#     print("Lisätään CORS-otsikoita...")
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
#     response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
#     print("CORS-otsikot lisätty.")
#     return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
