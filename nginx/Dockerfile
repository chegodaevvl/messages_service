FROM nginx

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY ./static .
