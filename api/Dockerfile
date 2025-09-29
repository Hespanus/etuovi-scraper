# Käytä virallista Python-kuvaa perustana
FROM python:3.9-slim

# Aseta työhakemisto
WORKDIR /app

# Kopioi vaaditut Python-riippuvuudet
COPY requirements.txt .

# Asenna Python-riippuvuudet
RUN pip install --no-cache-dir -r requirements.txt

# Kopioi Python-tiedostot sovellukseen (api.py)
COPY api.py .

# Paljasta portti, jossa sovellus kuuntelee
EXPOSE 5000

# Määrittele komento, joka ajetaan kun kontti käynnistyy (API)
CMD ["python", "api.py"]
