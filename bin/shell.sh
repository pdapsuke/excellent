#!/bin/bash

function usage {
cat >&2 <<EOS
開発環境でアプリを起動するコマンド

[usage]
 $0 -e ./local.env
  開発用シェルを起動（default）
 $0 -e ./prd.env
  本番用シェルを起動

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
    -e | --env    ) shift; ENV_PATH=$1;;
    -* | --*      ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

export $(cat $ENV_PATH | grep -v -e "^ *#")

export DOCKER_BUILDKIT=1
docker build \
  --build-arg host_uid=$USER_ID \
  --build-arg host_gid=$GROUP_ID \
  --rm \
  -f docker/dev/Dockerfile \
  -t excellent-app-dev:latest \
  .

LOCAL_APP_DIR="${PROJECT_ROOT}/app"

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