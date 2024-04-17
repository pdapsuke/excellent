## 開発環境について
[READMEに戻る](../README.md)

### 前提（初回デプロイ時のみ実行）
1. VPC, パブリックサブネット×2, プライベートサブネット×2を用意してください。
1. [パラメータシート](./parameter-sheet.md#cognito-ユーザープールパラメータ)に従って、Cognitoユーザープール, アプリケーションクライアントを作成してください。
1. 以下のコマンドを実行し、ECRを作成してください。  
※ホストにAWSCLIがインストール済み、クレデンシャル(`~/.aws/config`, `~/.aws/credentials` Administrator権限)が設定されている必要があります。EC2上で実行する場合はIAMロールへポリシーアタッチしてください。  
    ```shell
    # 変数定義
    APP_NAME="アプリケーション名"
    STAGE="ステージ名"  # ステージ名は半角英数字で5文字まで ex.STAGE=stg

    # 確認
    echo $APP_NAME $STAGE

    REPOSITORY_NAME="${APP_NAME}/${STAGE}/app"

    # リポジトリ作成
    aws ecr create-repository --repository-name $REPOSITORY_NAME
    ```
1. terraformのtfstate管理用S3バケットを作成してください。
    ```shell
    TFSTATE_BUCKET="XXXXX" # バケット名
    AWS_REGION="ap-northeast-1"

    aws s3api create-bucket \
    --bucket $TFSTATE_BUCKET \
    --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION
    ```
1. tfstate-lock用のdynamoDBテーブルを作成してください。
    ```shell
    TFSTATE_LOCK_TABLE="XXXXX" # dynamoDBテーブル名
    AWS_REGION="ap-northeast-1"

    aws dynamodb create-table \
        --table-name $TFSTATE_LOCK_TABLE \
        --attribute-definitions AttributeName=LockID,AttributeType=S \
        --key-schema AttributeName=LockID,KeyType=HASH \
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
        --region $AWS_REGION
    ```
1. Route53で任意のドメインを取得してください。[取得手順](https://docs.aws.amazon.com/ja_jp/Route53/latest/DeveloperGuide/domain-register.html#domain-register-procedure-section)
1. （オプション）ACMで証明書を発行してください。[取得手順](https://docs.aws.amazon.com/ja_jp/acm/latest/userguide/gs-acm-request-public.html)

#### terraform/envs/${STAGE}フォルダの作成
`terraform/envs/sample`フォルダを中のファイルごとコピーして、各ステージ用フォルダ(ex. `terraform/envs/stg`)を作成

#### terraformプロバイダ設定
`terraform/envs/${STAGE}/main.tf`
| パラメータ | 説明 |
| -- | -- |
| terraform.backend.s3.bucket | tfstate管理用S3バケット名に書き換えてください |
| terraform.backend.s3.dynamodb_table | tfstate-lock用のdynamoDBテーブル名に書き換えてください |
| provider.aws.default_tags.tags.PROJECT_NAME | 任意のプロジェクト名に書き換えてください |

### ECSイメージのプッシュ
```shell
# プロジェクトのルートディレクトリで実行
STAGE="ステージ名" # ex. stg
CONTAINER_IMAGE_TAG="イメージバージョン" # ex. latest

echo $STAGE $CONTAINER_IMAGE_VERSION 
./bin/image-push.sh -s $STAGE -t $CONTAINER_IMAGE_VERSION
```

### environment.auto.tfvarsの設定
[environment.auto.tfvarsのパラメータシート](./parameter-sheet.md#terraformデプロイ実行時入力待ちとなるパラメータ)を参考に、`terraform/envs/${STAGE}/environment.auto.tfvars`を実際の値に書き換えてください

### terraformコマンドの実行
※クライアントPCからデプロイするときはクレデンシャルファイルが必要（terraform-local-sample.envを参考）
```shell
# ロールに権限が付与されているEC2上で実行する場合は、--credential-fileオプションは不要
# コマンドのヘルプは-hオプションで確認
./bin/terraform.sh --stage $STAGE --credential-file ./terraform-local.env -- apply
```
WebアプリのURLはweb_urlとしてデプロイ後に出力され、問題なくアクセスできればデプロイ完了