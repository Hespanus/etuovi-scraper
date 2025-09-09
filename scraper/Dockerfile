# Käytä virallista Selenium-kuvaa, jossa on Chrome valmiiksi asennettuna
FROM docker.io/selenium/standalone-chrome:latest

# Aseta työhakemisto
WORKDIR /app

# Kopioi tarvittavat Python-riippuvuudet
COPY requirements.txt .

# Varmista, että pip asennetaan root-käyttäjänä
USER root

# Asenna Python-riippuvuudet
RUN pip install --no-cache-dir -r requirements.txt

# Palauta alkuperäinen käyttäjä, jos haluat ajaa sovelluksen ei-root-käyttäjänä
USER seluser

# Kopioi Python-tiedostot sovellukseen
COPY . .

# Paljasta portti, jossa sovellus kuuntelee
EXPOSE 5000

# Määrittele komento, joka ajetaan kun kontti käynnistyy
# Huom: Selenium-kuvassa on jo valmiiksi toimiva komentorivi
CMD ["python", "scraper_api.py"]