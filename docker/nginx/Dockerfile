FROM nginx:1.24.0-bullseye

ENV DEBIAN_FRONTEND=nointeractive

RUN apt-get update && apt-get install locales curl -y

RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

COPY ./docker/nginx/config/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/config/default.conf /etc/nginx/conf.d/default.conf