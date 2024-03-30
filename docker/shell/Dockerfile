FROM python:3.11-slim-bullseye

ARG host_uid
ARG host_gid

RUN apt update && \
    apt install -y locales curl default-mysql-client less vim net-tools iputils-ping sudo

# ロケール設定
RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# ユーザー作成
RUN groupadd -g $host_gid app && \
    useradd -u $host_uid -o -m -g $host_gid -s /bin/bash app && \
    echo "app ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/app

COPY docker/shell/.private_bashrc /home/app/.private_bashrc
RUN echo "source ~/.private_bashrc" >> /home/app/.bashrc

# Pythonライブラリインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# importの起点となるパスを環境変数として定義
ENV PYTHONPATH=/opt/app

CMD ["/bin/bash"]