from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# Haetaan API-palvelun osoite ympäristömuuttujasta
# "http://api-service:5000" on Kubernetesin sisäinen osoite, joka toimii vain klusterin sisällä
API_SERVICE_URL = 'http://api-service:5000'

app = Flask(__name__)
# Tämä asetus sallii CORS-pyynnöt selaimelta
CORS(app)

@app.route('/')
def home():
    return "Web-palvelin käynnissä!"

# Välityspalvelimen päätepiste, joka välittää pyynnön API-palvelimelle
@app.route('/api/trigger-scraper', methods=['POST'])
def trigger_scraper():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL-osoite puuttuu.'}), 400

    try:
        # Välitetään pyyntö API-palvelulle
        # Tämä pyyntö tapahtuu klusterin sisäisesti, joten CORS-ongelmaa ei synny
        response = requests.post(f'{API_SERVICE_URL}/trigger-scraper', json={'url': url})
        response.raise_for_status()

        # Palautetaan suoraan API-palvelimen vastaus
        return Response(response.content, status=response.status_code, mimetype=response.headers['Content-Type'])

    except requests.exceptions.RequestException as e:
        print(f"Virhe pyynnössä API-palvelimelle: {e}")
        return jsonify({'error': 'Virhe pyynnössä API-palvelimelle.'}), 500

if __name__ == '__main__':
    # Ajetaan palvelin portissa 5000, mutta kuunnellaan kaikkia IP-osoitteita (0.0.0.0)
    app.run(debug=True, host='0.0.0.0', port=5000)
