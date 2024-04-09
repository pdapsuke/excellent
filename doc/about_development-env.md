## 開発環境について
[READMEに戻る](../README.md)

### 前提
- 開発環境の構築には、docker, docker-composeのインストールが事前に必要です。
- cognitoのuserpoolを構築しておく必要があります。  
設定値はパラメータシートを参照

### local.envの作成
sample.envのパラメータを書き換えて、local.envを作成してください。
```shell
DB_USER=root
DB_PASSWORD=root1234
DB_NAME=local
DB_HOST=127.0.0.1
DB_PORT=63306
AWS_REGION=<your_cognito_region>
COGNITO_USERPOOL_ID=<your_cognito_userpool_id>
COGNITO_CLIENT_ID=<your_cognito_client_id>
FIND_PLACE_URL=https://maps.googleapis.com/maps/api/place/textsearch/json
PLACE_DETAILS_URL=https://maps.googleapis.com/maps/api/place/details/json
MODE=local
FIND_PLACE_API_KEY=<your_find_place_api_key>
PHOTO_REFERENCE_URL=https://maps.googleapis.com/maps/api/place/photo
DB_SECRET_NAME=XXXXXXXX
RESAS_API_PREFECTURE_URL=https://opendata.resas-portal.go.jp/api/v1/prefectures
RESAS_API_CITY_URL=https://opendata.resas-portal.go.jp/api/v1/cities
RESAS_API_KEY=<your_resas_api_key>
```
#### 補足
- AWS_REGION: cognito userpoolがあるリージョン ex. ap-northeast-1
- FIND_PLACE_API_KEY: google map APIのキー  
  [Places APIキー作成方法](https://developers.google.com/maps/documentation/javascript/places?hl=ja)を参考にAPIキーの発行、サービスの割り当てをしてください。
- RESAS_API_KEY: RESAS APIのキー  
[RESAS APIの利用登録](https://opendata.resas-portal.go.jp/form.html)を参考にAPIキーを発行してください。
### 開発用データベースの起動
```shell
./bin/mysql.sh
```

### データベースの初期化
```shell
#開発用シェルを起動
./bin/shell.sh
```

開発用シェル内での操作
```shell
# データベースの初期化
# データベースのcreate, テーブル定義のマイグレーションまで実行される
./bin/init-database.sh
```

### アプリの起動
開発用シェルからexitした状態で実行
```shell
# docker-composeによってnuxt3, fastapi, nginxのコンテナが起動する
# アプリの画面：http://localhost
# fastapiのデバッグ画面：http://localhost:8018/docs
./bin/run.sh
```
