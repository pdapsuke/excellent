FROM python:3.11-slim-bullseye

RUN apt update && \
    apt install -y locales curl default-mysql-client less vim net-tools iputils-ping sudo

# ロケール設定
RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# install nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs

# アプリのソースコード
COPY app /opt/app

COPY docker/front/entrypoint-front.sh /entrypoint-front.sh
RUN chmod +x /entrypoint*.sh
CMD ["/entrypoint-front.sh"]