# Käytä virallista Nginx-kuvaa pohjana
FROM docker.io/nginx:1.21.6-alpine

# Asenna Python 3 ja pip
RUN apk add --no-cache python3 py3-pip

# Asenna Python-kirjastot
RUN pip install flask requests gunicorn flask_cors python-dotenv

# Aseta työhakemisto
WORKDIR /usr/share/nginx/html

# Kopioi proxy-sovellus kansioon
COPY ./proxy_api.py /app/proxy_api.py

# Aseta nginx-konfiguraatio
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Kopioi HTML-, CSS- ja JS-tiedostot
COPY ./index.html ./
COPY ./script.js ./
COPY ./style.css ./

# Oletuskomento, joka käynnistää Gunicornin ja Nginxin taustalla
CMD python3 /app/proxy_api.py & nginx -g 'daemon off;'
