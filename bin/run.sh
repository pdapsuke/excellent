#!/bin/bash

function usage {
cat >&2 <<EOS
開発環境でアプリを起動するコマンド

[usage]
 $0 -e ./local.env
  開発DB, APIキーでアプリを起動（default）
 $0 -e ./prd.env
  本番DB, APIキーでアプリを起動

[options]
 -h | --help:
   ヘルプを表示
 -e | --env <env file path>:
EOS
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

ENV_PATH="${PROJECT_ROOT}/local.env"
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

export $(cat $ENV_PATH | grep -v -e "^ *#")

# Dockerイメージを複数生成するためビルド処理を関数化
build_image() {
  DOCKERFILE_PATH="$1"
  DOCKER_IMAGE_TAG="$2"

  docker build \
    --build-arg host_uid=$USER_ID \
    --build-arg host_gid=$GROUP_ID \
    --rm \
    -f $DOCKERFILE_PATH \
    -t $DOCKER_IMAGE_TAG \
    .
}

export DOCKER_BUILDKIT=1
build_image "docker/front-dev/Dockerfile" "excellent-app-front-dev:latest" # フロントは開発用コンテナをビルドする
build_image "docker/api/Dockerfile" "excellent-app-api:latest"
build_image "docker/nginx/Dockerfile" "excellent-app-nginx:latest"

LOCAL_APP_DIR="${PROJECT_ROOT}/app"

export LOCAL_APP_DIR="$LOCAL_APP_DIR"
export ENV_PATH="$ENV_PATH"

cd "${PROJECT_ROOT}/docker"
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up