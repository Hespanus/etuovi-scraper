from flask import Flask, jsonify, request
from etuovi_scrape import run_scraper 

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_job():
    # Vastaanota JSON-data POST-pyynnön rungosta
    data = request.get_json()
    url = data.get('url')  # Haetaan 'url'-avain sanakirjasta

    # Tarkista, että URL-osoite on olemassa
    if not url:
        return jsonify({'error': 'URL-osoite puuttuu pyynnöstä.'}), 400

    try:
        # Kutsu scraper-funktiota ja välitä sille URL-osoite
        scraped_data = run_scraper(url)        
        return jsonify(scraped_data), 200
    except Exception as e:
        print(f"Scraper-funktiossa tapahtui virhe: {e}")
        return jsonify({'error': f'Virhe scraperissa: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)