// VPCのID
vpc_id = "XXXXX"

// RDSを配置するためのサブネット
private_subnets = ["XXXXX", "XXXXX"]

// DBのユーザー名, PW
db_user     = "XXXXX"
db_password = "XXXXX"

// cognitoのユーザープール、クライアントID
cognito_userool_id = "ap-northeast-1_XXXXX"
cognito_client_id  = "XXXXXX"

// googlemapのapiキー
find_place_api_key = "XXXXX"

// resas apiのapiキー
resas_api_key = "XXXXX"

// フロント, バックエンド, nginxの各コンテナイメージのURI
front_app_image_uri = "XXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/XXXXX"
api_app_image_uri   = "XXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/XXXXX"
nginx_app_image_uri = "XXXXX.dkr.ecr.ap-northeast-1.amazonaws.com/XXXXX"

// ALB, ECSを配置するサブネット
public_subnets = ["subnet-XXXXX", "subnet-XXXXX"]

// ALBのエイリアスレコードを管理するホストゾーンのID
hostzone_id = "XXXXX"

// ALBのエイリアスレコードを管理するホストゾーンのID
hostzone_name = "XXXXX.XXX"

// 証明書のARN
certificate_arn = ""
