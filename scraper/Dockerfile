# Käytä virallista Selenium-kuvaa, jossa on Chrome valmiiksi asennettuna
FROM selenium/standalone-chrome:latest

# Aseta työhakemisto
WORKDIR /app

# Kopioi tarvittavat Python-riippuvuudet
COPY requirements.txt .

# Asenna Python-riippuvuudet
RUN pip install --no-cache-dir -r requirements.txt

# Kopioi Python-tiedostot sovellukseen
COPY . .

# Paljasta portti, jossa sovellus kuuntelee
EXPOSE 5000

# Määrittele komento, joka ajetaan kun kontti käynnistyy
# Huom: Selenium-kuvassa on jo valmiiksi toimiva komentorivi
CMD ["python", "scraper_api.py"]