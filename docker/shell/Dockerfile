FROM python:3.11-slim-bookworm

ARG host_uid
ARG host_gid

RUN apt update && \
    apt install -y locales curl unzip default-mysql-client less vim net-tools iputils-ping sudo jq

# ロケール設定
RUN echo 'ja_JP.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=ja_JP.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# aws cli インストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

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