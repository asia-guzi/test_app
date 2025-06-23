# Używamy oficjalnego obrazu Nginx
FROM nginx:alpine

# Folder w kontenerze, gdzie Nginx szuka plików statycznych
WORKDIR /usr/share/nginx/html

# Usuń domyślne pliki statyczne Nginx, jeśli takie istnieją
RUN rm -rf ./*

# Skopiuj statyczne pliki frontendowe do kontenera
COPY ./ /usr/share/nginx/html


# Skopiuj nasz własny config dla Nginx
COPY default.conf /etc/nginx/conf.d/default.conf