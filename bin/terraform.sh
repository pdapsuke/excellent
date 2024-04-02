function usage {
cat >&2 <<EOF
terraformコマンド
[usage]
$0 [options] -- [TF_ARGS1] [TF_ARGS2] [TF_ARGS3] ...

[options]
  -h | --help
  -s | --stage <STAGE_NME>: {required}
    terraformのステージ名を指定
  -c | --credential-file <CREDENTIAL_PATH>
    クライアントPCなどAWS環境外からデプロイする場合は、認証情報（IAMユーザー アクセスキー/シークレットアクセスキー）
    を記載したenvファイルをterraformコンテナに渡す

[example]
  ヘルプ
    $0 --stage prd --help
  初期化
    $0 --stage prd -- init
  デプロイ
    $0 --stage prd -- apply
  クライアントPCからデプロイ
    $0 --stage prd --credential-file ./terraform-local.env -- apply
EOF
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
echo $PROJECT_ROOT
cd "$PROJECT_ROOT"

USE_CREDENTIAL_FILE=
CREDENTIAL_PATH=
STAGE=
TERRAFORM_ARGS=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help            ) usage;;
    -s | --stage           ) shift; STAGE="$1" ;;
    -c | --credential-file ) shift; USE_CREDENTIAL_FILE=1 && CREDENTIAL_PATH="$1";;  
    --                     ) shift; TERRAFORM_ARGS+=($@); break;;
    -* | --*               ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

echo "stage: $STAGE"
echo "terraform_args: $TERRAFORM_ARGS"

[ -z "$STAGE" ] && echo "--stageオプションを指定してください"

# docker run コマンドの組み立て
DOCKER_RUN_CMD="docker run -ti --rm"
# クレデンシャルファイルを使用する場合、docker runコマンドに--env-fileオプションを追加
if [ $USE_CREDENTIAL_FILE -eq 1 ]; then
  [ ! -e "$CREDENTIAL_PATH" ] && echo "指定したクレデンシャルファイル($CREDENTIAL_PATH)は存在しません" >&2 && exit 1
  DOCKER_RUN_CMD="$DOCKER_RUN_CMD --env-file \"$CREDENTIAL_PATH\""
fi
DOCKER_RUN_CMD="$DOCKER_RUN_CMD --user app -w /terraform/envs/$STAGE -v ${PROJECT_ROOT}/terraform:/terraform excellent-terraform:latest ${TERRAFORM_ARGS[@]}"

set -e

# イメージビルド
docker build \
  --rm \
  --build-arg host_uid=$(id -u) \
  --build-arg host_gid=$(id -g) \
  -f docker/terraform/Dockerfile \
  -t excellent-terraform:latest .

# 組み立てたdocker runコマンドを実行
eval "$DOCKER_RUN_CMD"