variable "app_name" {}
variable "stage" {}
variable "account_id" {}

// ECSタスクのコンテナイメージのURI(フロントエンド)
variable "front_app_image_uri" {}

// ECSタスクのコンテナイメージのURI(バックエンド)
variable "api_app_image_uri" {}

// ECSタスクのコンテナイメージのURI(nginx)
variable "nginx_app_image_uri" {}

// コンテナイメージのバージョン
variable "container_image_version" { type = string }

// ECSのセキュリティグループ・ALBのターゲットグループを作成するVPC
variable "vpc_id" {}

// ECSタスクを起動するサブネット
variable "subnets" { type = list(string) }

// ECSのセキュリティグループで許可するCIDRブロック
variable "ingress_cidr_blocks" {
  type = list(string)
}

// apiコンテナの環境変数
variable "env_api" { type = map(any) }

// frontコンテナの環境変数
variable "env_front" { type = map(any) }

// apiコンテナのsecret
variable "secrets_api" { type = map(any) }

// frontコンテナのsecret
variable "secrets_front" { type = map(any) }

// HTTPSでアクセスする場合のSSL証明書のARN
variable "certificate_arn" {
  type        = string
  default     = ""
  description = "SSL証明書のARN。空文字の場合はHTTPのリスナーを作成する"
}

locals {
  // certificate_arnが指定されていたら "1"
  use_https_listener = length(var.certificate_arn) > 0 ? "1" : "0"
  // certificate_arnが指定されていたら "0"
  use_http_listener  = length(var.certificate_arn) <= 0 ? "1" : "0"
  front_container_name     = "front"
  front_container_port     = 3000
  api_container_name     = "api"
  api_container_port     = 8018
  nginx_container_name     = "nginx"
  nginx_container_port     = 80
}

// アプリ用ALBのARN
variable "app_alb_arn" {}

// 固定レスポンス用ALBのARN
variable "fixed_response_alb_arn" {}