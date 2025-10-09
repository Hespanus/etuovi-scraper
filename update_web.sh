#!/bin/bash

# Tämä skripti rakentaa uuden web-app-kuvan ja puskuttaa sen rekisteriin.
# VAADITAAN: Docker Desktop käynnissä. kubectl-komennot on suoritettava erikseen Linux/Ubuntu-ympäristöstä.

# --- MUOKKAA NÄITÄ ARVOJA ---

# 1. WEB-sovelluksen kansion polku. Tämän TÄYTYY osoittaa web-service-kansioon, 
# jossa Dockerfile ja script.js sijaitsevat. Käytä Bash-muotoa (esim. /c/...).
# Oletetaan, että ajat skriptin projektin juuresta:
WEB_DIR="./web" 

# 2. Kuvan nimi ja rekisteri. Varmista, että nämä vastaavat Kubernetes-deploymentia.
IMAGE_NAME="web-service"
REGISTRY_URL="registry.digitalocean.com/heikkiregistry"

# ----------------------------

FULL_IMAGE_NAME="${REGISTRY_URL}/${IMAGE_NAME}"

# Tarkistetaan, onko Docker käynnissä
if ! command -v docker &> /dev/null; then
    echo "Virhe: 'docker'-komentoa ei löydy. Varmista, että Docker Desktop on asennettu ja PATH-muuttujassa."
    exit 1
fi

# Tarkista, onko kansio olemassa
if [ ! -d "$WEB_DIR" ]; then
  echo "Virhe: Kansiota '$WEB_DIR' ei löydy. Varmista WEB_DIR-polku skriptissä. Lopetetaan."
  exit 1
fi

echo "--- DOKS WEB-APP PÄIVITYS ALOITETTU ---"
echo "Työhakemisto: $WEB_DIR"

# Siirrytään kansioon (tarpeellinen docker build -komentoa varten)
cd "$WEB_DIR" || exit

# Vaihe 1: Rakennetaan uusi Docker-kuva
# HUOM: Käytetään nykyistä hakemistoa (.).
echo "1. Rakennetaan uusi kuva: ${FULL_IMAGE_NAME}:latest"
docker build -t "${IMAGE_NAME}:latest" .

if [ $? -ne 0 ]; then
  echo "Virhe: Kuvan rakentaminen epäonnistui. Lopetetaan."
  exit 1
fi

# Vaihe 2: Taggataan kuva rekisteriä varten
echo "2. Taggataan kuva: ${FULL_IMAGE_NAME}:latest"
docker tag "${IMAGE_NAME}:latest" "${FULL_IMAGE_NAME}:latest"

# Vaihe 3: Pusketaan kuva DigitalOcean Container Registryyn
echo "3. Pusketaan kuva rekisteriin: ${FULL_IMAGE_NAME}:latest"
# TÄRKEÄÄ: Sinun täytyy olla kirjautuneena tähän rekisteriin (docker login registry.digitalocean.com)
docker push "${FULL_IMAGE_NAME}:latest"

if [ $? -ne 0 ]; then
  echo "Virhe: Kuvan puskeminen epäonnistui. Oletko kirjautunut rekisteriin? Lopetetaan."
  exit 1
fi

# Siirrytään takaisin alkuperäiseen hakemistoon (jotta terminaali on samassa paikassa)
cd - > /dev/null 2>&1

echo "--- DOKS WEB-APP PÄIVITYS VALMIS (Vaiheet 1-3) ---"
echo ""
echo "################################################################"
echo "### TÄRKEÄÄ: SUORITA SEURAAVA KOMENTO MANUAALISESTI UBUNTUSSA ###"
echo "################################################################"
echo ""
echo "Siirry Ubuntu/WSL-terminaaliin ja aja Deploymentin uudelleenkäynnistys:"
echo "kubectl rollout restart deployment web-deployment"
echo ""
echo "Kun uusi podi on käynnissä, käynnistä selaimessa kova päivitys (Ctrl+Shift+R) ja tarkista konsoli."
