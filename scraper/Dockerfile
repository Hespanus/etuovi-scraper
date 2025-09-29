# Käytä virallista Selenium-kuvaa, jossa on Chrome valmiiksi asennettuna
FROM docker.io/selenium/standalone-chrome:latest

# Aseta työhakemisto
WORKDIR /app

# Kopioi tarvittavat Python-riippuvuudet
COPY requirements.txt .

# Varmista, että pip asennetaan root-käyttäjänä (tyypillistä tässä kuvassa)
USER root

# Asenna Python-riippuvuudet
RUN pip install --no-cache-dir -r requirements.txt

# Palauta alkuperäinen käyttäjä, jos mahdollista (seluser)
USER seluser

# Kopioi Python-tiedostot sovellukseen
COPY scraper_api.py .
COPY etuovi_scrape.py . 

# Paljasta portti, jossa sovellus kuuntelee (VALITSE ERI PORTTI KUIN API)
EXPOSE 5001

# Määrittele komento, joka ajetaan kun kontti käynnistyy
# HUOM: Oletetaan, että scraper_api.py käynnistää Python-sovelluksen
CMD ["python", "scraper_api.py"]
