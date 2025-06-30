
FROM nginx:alpine

# Folder for static files
WORKDIR /usr/share/nginx/html

# remove default Nginx files
RUN rm -rf ./*

# copy frontend files
COPY ./ /usr/share/nginx/html

# config for Nginx
COPY default.conf /etc/nginx/conf.d/default.conf