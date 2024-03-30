FROM python:3.11-slim-bookworm

RUN apt update && \
    apt install -y locales curl default-mysql-client less vim net-tools iputils-ping sudo

# ロケール設定
RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# Pythonライブラリインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリのソースコード
COPY app /opt/app

# importの起点となるパスを環境変数として定義
ENV PYTHONPATH=/opt/app

COPY docker/api/entrypoint-api.sh /entrypoint-api.sh
RUN chmod +x /entrypoint*.sh
CMD ["/entrypoint-api.sh"]