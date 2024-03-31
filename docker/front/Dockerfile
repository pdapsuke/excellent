FROM node:20-bookworm-slim

# アプリのソースコード
COPY app/front /opt/app/front

COPY docker/front/entrypoint-front.sh /entrypoint-front.sh
RUN chmod +x /entrypoint*.sh

RUN cd /opt/app/front &&\
    npm install

CMD ["/entrypoint-front.sh"]