# Käytä virallista Nginx-kuvaa, joka on pieni ja nopea
FROM docker.io/nginx:1.21.6-alpine

# Kopioi HTML-, CSS- ja JS-tiedostot Nginxin oletushakemistoon
# Oletan, että nämä tiedostot ovat samassa hakemistossa kuin Dockerfile
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY script.js /usr/share/nginx/html/script.js

# Korvataan Nginxin oletuskonfiguraatio, jotta voidaan palvella tiedostoja
# HUOM: Tässä EI OLE ENÄÄ proxya, koska se siirtyy Kubernetes Ingressiin!
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nginx kuuntelee oletuksena porttia 80
EXPOSE 80

# Oletuskomento käynnistää Nginxin
CMD ["nginx", "-g", "daemon off;"]