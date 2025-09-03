from flask import Flask, jsonify, request, Response
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Lataa ympäristömuuttujat .env-tiedostosta
load_dotenv()

# Haetaan scraper-palvelun osoite ympäristömuuttujasta
SCRAPER_SERVICE_URL = os.getenv("SCRAPER_SERVICE_URL", "http://scraper-service:5001")

app = Flask(__name__)
CORS(app)

# Tervehdys-päätepiste (voit tarkistaa, että API on käynnissä)
@app.route('/')
def home():
    return "API-palvelin käynnissä!"

# Scraperin käynnistys-päätepiste
@app.route('/trigger-scraper', methods=['POST'])
def trigger_scraper():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL-osoite puuttuu.'}), 400

    try:
        # Välitetään pyyntö scraper-palvelulle
        # stream=True ensures we can handle the response efficiently
        response = requests.post(f'{SCRAPER_SERVICE_URL}/run', json={'url': url}, stream=True)
        response.raise_for_status()  # Tarkistaa HTTP-virheet

        # # --- UUDET DEBUG-TULOSTEET TÄSSÄ ---
        # print("\n--- Vastaus Scraperilta (API-palvelimessa) ---")
        # print(f"Statuskoodi: {response.status_code}")
        # print(f"Vastauksen tyyppi: {response.headers['Content-Type']}")
        # # Vastauksen sisältö voidaan lukea .text- tai .content-ominaisuudesta
        # # Käytetään .text:iä luettavuuden vuoksi, koska odotamme JSON-dataa
        # print("Vastauksen sisältö:")
        # print(response.text)
        # print("-----------------------------------------------\n")
        
        # # Palautetaan suoraan scraperin vastaus ilman turhaa uudelleenmuotoilua
        return Response(response.content, status=response.status_code, mimetype=response.headers['Content-Type'])
    
    except requests.exceptions.RequestException as e:
        print(f"Virhe pyynnössä scraperiin: {e}")
        return jsonify({'error': f'Virhe pyydettäessä scraperia: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)