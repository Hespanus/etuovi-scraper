# Käytä virallista Python-kuvaa perustana
FROM python:3.9-slim

# Aseta työhakemisto
WORKDIR /app

# Kopioi vaaditut Python-riippuvuudet
# Huom: Tässä käytämme samaa parasta käytäntöä kuin scraperin kanssa
COPY requirements.txt .

# Asenna Python-riippuvuudet
RUN pip install --no-cache-dir -r requirements.txt

# Kopioi Python-tiedostot sovellukseen
COPY . .

# Paljasta portti, jossa sovellus kuuntelee
EXPOSE 5000

# Määrittele komento, joka ajetaan kun kontti käynnistyy
# Huom: app.py käynnistää Flask-sovelluksen
CMD ["python", "api.py"]