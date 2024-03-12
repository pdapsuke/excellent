#!/bin/bash

function usage {
cat <<EOF >&2
[USAGE]
  $0 --stage <STAGE>
EOF
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
cd "$PROJECT_ROOT"

STAGE=
args=()
while [ "$#" != 0 ]; do
  case $1 in
    -s | --stage ) shift; STAGE="$1" ;;
    -* | --*     ) echo "不正なオプション: $1" >&2; exit 1 ;;
    *            ) args+=("$1") ;;
  esac
  shift
done

[ "${#args[@]}" != 0 ] && usage
[ -z "$STAGE" ] && usage

set -e

REPOSITORY_NAME="excellent/${STAGE}/app"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
AWS_REGION="ap-northeast-1"


# イメージビルド
docker build --rm -f docker/front/Dockerfile -t ${REPOSITORY_NAME}-front:latest .
docker build --rm -f docker/api/Dockerfile -t ${REPOSITORY_NAME}-api:latest .
docker build --rm -f docker/nginx/Dockerfile -t ${REPOSITORY_NAME}-nginx:latest .

# ECRにログイン
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# ECRにフロントイメージをpush
REMOTE_REPOSITORY_NAME_FRONT=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}-front:latest
docker tag ${REPOSITORY_NAME}-front:latest $REMOTE_REPOSITORY_NAME_FRONT
docker push $REMOTE_REPOSITORY_NAME_FRONT

# ECRにapiイメージをpush
REMOTE_REPOSITORY_NAME_API=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}-api:latest
docker tag ${REPOSITORY_NAME}-api:latest $REMOTE_REPOSITORY_NAME_API
docker push $REMOTE_REPOSITORY_NAME_API

# ECRにnginxイメージをpush
REMOTE_REPOSITORY_NAME_NGINX=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}-nginx:latest
docker tag ${REPOSITORY_NAME}-nginx:latest $REMOTE_REPOSITORY_NAME_NGINX
docker push $REMOTE_REPOSITORY_NAME_NGINX