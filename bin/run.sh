#!/bin/bash

function usage {
cat >&2 <<EOS
コンテナ起動コマンド

[usage]
 $0 <CHAPTER> [options]

[options]
 -h | --help:
   ヘルプを表示
 -m | --mode <MODE>:
  起動モードを指定
  MODE:
    app
      fastapiを起動 (default)
    shell
      コンテナにshellでログイン

[example]
 アプリを起動する
   $0
   $0 --mode app
 shellを起動する
   $0 --mode shell
EOS
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

ENV_PATH="${PROJECT_ROOT}/local.env"
RUN_MODE="app"
USER_ID=$(id -u)
GROUP_ID=$(id -g)
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help   ) usage;;
    -m | --mode   ) shift; RUN_MODE=$1;;
    -e | --env    ) shift; ENV_PATH=$1;;
    -* | --*      ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

if [ "$RUN_MODE" != "app" -a "$RUN_MODE" != "shell" ]; then
  echo "--mode には app, shellのいずれかを指定してください" >&2
  exit 1
fi

export $(cat $ENV_PATH | grep -v -e "^ *#")

# Docker build app server
export DOCKER_BUILDKIT=1
docker build \
  --build-arg host_uid=$USER_ID \
  --build-arg host_gid=$GROUP_ID \
  --rm \
  -f docker/dev/Dockerfile \
  -t excellent-app-dev:latest \
  .

docker build \
  --build-arg host_uid=$USER_ID \
  --build-arg host_gid=$GROUP_ID \
  --rm \
  -f docker/nginx/Dockerfile \
  -t excellent-nginx-dev:latest \
  .

LOCAL_APP_DIR="${PROJECT_ROOT}/app"

export LOCAL_APP_DIR="$LOCAL_APP_DIR"
export ENV_PATH="$ENV_PATH"

if [ "$RUN_MODE" = "shell" ]; then
  docker run \
    --rm \
    -ti \
    --network host \
    --env-file "$ENV_PATH" \
    -e "DB_NAME=$DB_NAME" \
    -w /opt/app \
    --user="$USER_ID:$GROUP_ID" \
    -v ${LOCAL_APP_DIR}:/opt/app \
    excellent-app-dev:latest \
    "/bin/bash"
else
  cd "${PROJECT_ROOT}/docker"
  docker-compose -f docker-compose.yml down
  docker-compose -f docker-compose.yml up
fi
