function usage {
cat >&2 <<EOF
terraformコマンド
[usage]
$0 [options] -- [TF_ARGS1] [TF_ARGS2] [TF_ARGS3] ...

[options]
  -h | --help
  --stage <STAGE_NME>: {required}
    terraformのステージ名を指定

[example]
  ヘルプ
    $0 --stage prd --help
  初期化
    $0 --stage prd -- init
  環境とソースコードの差分確認
    $0 --stage prd -- plan
  デプロイ
    $0 --stage prd -- apply
  削除
    $0 --stage prd -- destroy
EOF
exit 1
}

PROJECT_ROOT="$(cd $(dirname $0)/..; pwd)"
echo $PROJECT_ROOT
cd "$PROJECT_ROOT"

ENV_PATH="${PROJECT_ROOT}/terraform-local.env"
STAGE=
TERRAFORM_ARGS=()
while [ "$#" != 0 ]; do
  case $1 in
    -h | --help ) usage ;;
    -s | --stage ) shift; STAGE="$1" ;;
    -- ) shift; TERRAFORM_ARGS+=($@); break ;;
    -* | --* ) echo "$1 : 不正なオプションです" >&2; exit 1;;
  esac
  shift
done

[ -z "$STAGE" ] && echo "--stageオプションを指定してください"

set -e

# イメージビルド
docker build \
  --rm \
  --build-arg host_uid=$(id -u) \
  --build-arg host_gid=$(id -g) \
  -f docker/terraform/Dockerfile \
  -t excellent-terraform:latest .

docker run -ti --rm \
  --env-file "$ENV_PATH" \
  --user app \
  -w /terraform/envs/$STAGE \
  -v ${PROJECT_ROOT}/terraform:/terraform \
  excellent-terraform:latest \
  ${TERRAFORM_ARGS[@]} \