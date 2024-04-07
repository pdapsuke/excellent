#!/bin/bash

function usage {
cat <<EOF >&2
[USAGE]
  $0 -s | --stage <STAGE> -t | --tag <IMAGE_TAG>
  $0 -s stg -t latest
EOF
exit 1
}
PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

STAGE=
IMAGE_TAG=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help  ) usage;;
    -s | --stage ) shift; STAGE="$1" ;;
    -t | --tag   ) shift; IMAGE_TAG="$1" ;;
    -* | --*     ) echo "不正なオプション: $1" >&2; exit 1 ;;
    *            ) args+=("$1") ;;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "$STAGE" ] && usage
[ -z "$IMAGE_TAG" ] && usage

set -e

# プッシュ先のリポジトリ名を定義
REPOSITORY_NAME="excellent/${STAGE}/app"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
AWS_REGION="ap-northeast-1"
REMOTE_REPOSITORY_PREFIX="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}"

# ECRにログイン
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# ビルドとプッシュの手順を関数化
build_and_push_image() {
  IMAGE_NAME="$1"
  DOCKERFILE_PATH="$2"
  REMOTE_IMAGE_NAME="$REMOTE_REPOSITORY_PREFIX-$IMAGE_NAME:$IMAGE_TAG"

  docker build --rm -f "$DOCKERFILE_PATH" -t "$REMOTE_IMAGE_NAME" .
  docker push "$REMOTE_IMAGE_NAME"
}

# Dockerイメージのビルドとプッシュ
build_and_push_image "front" "docker/front/Dockerfile"
build_and_push_image "api" "docker/api/Dockerfile"
build_and_push_image "nginx" "docker/nginx/Dockerfile"