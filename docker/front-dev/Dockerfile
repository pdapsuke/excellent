FROM node:20-bookworm-slim

# アプリのソースコード
COPY app/front /opt/app/front

COPY docker/front-dev/entrypoint-front-dev.sh /entrypoint-front-dev.sh
RUN chmod +x /entrypoint*.sh
CMD ["/entrypoint-front-dev.sh"]