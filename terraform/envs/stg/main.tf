terraform {
  required_providers {
    // AWS Provider: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  // terraformのバージョン指定
  required_version = ">= 1.2.0"

  // tfstateファイルをs3で管理する
  backend "s3" {
    // tfstate保存先のs3バケットとキー
    bucket  = "excellent-stg-bucket"
    region  = "ap-northeast-1"
    key     = "tfstate/terraform.tfstate"
    encrypt = true
    // tfstateファイルのロック情報をDynamoDBで管理する
    dynamodb_table = "excellent-stg-lock-table"
  }
}

provider "aws" {
  region = "ap-northeast-1"

  // すべてのリソースにデフォルトで設定するタグ
  default_tags {
    tags = {
      PROJECT_NAME = "EXCELLENT_STG"
    }
  }
}

// Terraformが認可されているアカウントの情報を取得するデータソース
data "aws_caller_identity" "self" {}

// 現在のリージョンを取得するデータソース
data "aws_region" "current" {}

// ローカル変数を定義
locals {
  aws_region                  = data.aws_region.current.name
  account_id                  = data.aws_caller_identity.self.account_id
  app_name                    = replace(lower("excellent"), "-", "")
  stage                       = "stg"
  vpc_cidr_block              = "192.168.0.0/16"
  nuxt_client_base_url_suffix = "://${module.route53_record.route53_record_app_alb.name}/api/v1"
  find_place_url              = "https://maps.googleapis.com/maps/api/place/textsearch/json"
  place_details_url           = "https://maps.googleapis.com/maps/api/place/details/json"
  photo_reference_url         = "https://maps.googleapis.com/maps/api/place/photo"
  resas_api_prefecture_url    = "https://opendata.resas-portal.go.jp/api/v1/prefectures"
  resas_api_city_url          = "https://opendata.resas-portal.go.jp/api/v1/cities"
}

// 変数定義
variable "vpc_id" { type = string }
variable "private_subnets" { type = list(string) }
variable "front_app_image_uri" { type = string }
variable "api_app_image_uri" { type = string }
variable "nginx_app_image_uri" { type = string }
variable "public_subnets" { type = list(string) }
variable "hostzone_id" { type = string }
variable "hostzone_name" { type = string }
variable "certificate_arn" { type = string }
variable "db_user" { type = string }
variable "db_password" { type = string }
variable "cognito_userool_id" { type = string }
variable "cognito_client_id" { type = string }
variable "find_place_api_key" { type = string }
variable "resas_api_key" { type = string }

output "env_secrets_manager_arn" {
  value = module.secrets.env_secrets_manager_arn
}

output "db_secrets_manager_arn" {
  value = module.secrets.db_secrets_manager_arn
}

module "db" {
  source              = "../../modules/db"
  app_name            = local.app_name
  stage               = local.stage
  vpc_id              = var.vpc_id
  private_subnets     = var.private_subnets
  db_name             = local.stage
  db_user             = var.db_user
  db_password         = var.db_password
  ingress_cidr_blocks = [local.vpc_cidr_block]
  instance_num        = 1
}

module "app" {
  source                 = "../../modules/app"
  app_name               = local.app_name
  stage                  = local.stage
  account_id             = local.account_id
  front_app_image_uri    = var.front_app_image_uri
  api_app_image_uri      = var.api_app_image_uri
  nginx_app_image_uri    = var.nginx_app_image_uri
  vpc_id                 = var.vpc_id
  subnets                = var.public_subnets
  ingress_cidr_blocks    = [local.vpc_cidr_block]
  app_alb_arn            = module.alb.app_alb.arn
  fixed_response_alb_arn = module.alb.fixed_response_alb.arn
  certificate_arn        = var.certificate_arn
  env_api = {
    "MODE" : local.stage,
    "DB_NAME" : local.stage,
    "DB_SECRET_NAME" : "/${local.app_name}/${local.stage}/db",
    "AWS_REGION" : local.aws_region,
    "FIND_PLACE_URL" : "${local.find_place_url}",
    "PLACE_DETAILS_URL" : "${local.place_details_url}",
    "PHOTO_REFERENCE_URL" : "${local.photo_reference_url}",
    "RESAS_API_PREFECTURE_URL" : "${local.resas_api_prefecture_url}",
    "RESAS_API_CITY_URL" : "${local.resas_api_city_url}",
  }
  env_front = {
    "AWS_REGION" : local.aws_region,
    "NUXT_CLIENT_BASE_URL" : length(var.certificate_arn) > 0 ? "https${local.nuxt_client_base_url_suffix}" : "http${local.nuxt_client_base_url_suffix}"
  }
  secrets_api = {
    "COGNITO_USERPOOL_ID" : "${module.secrets.env_secrets_manager_arn}:cognito_userool_id::",
    "COGNITO_CLIENT_ID" : "${module.secrets.env_secrets_manager_arn}:cognito_client_id::",
    "FIND_PLACE_API_KEY" : "${module.secrets.env_secrets_manager_arn}:find_place_api_key::",
    "RESAS_API_KEY" : "${module.secrets.env_secrets_manager_arn}:resas_api_key::",
  }
  secrets_front = {
    "COGNITO_USERPOOL_ID" : "${module.secrets.env_secrets_manager_arn}:cognito_userool_id::",
    "COGNITO_CLIENT_ID" : "${module.secrets.env_secrets_manager_arn}:cognito_client_id::",
  }
}

module "alb" {
  source         = "../../modules/alb"
  app_name       = local.app_name
  stage          = local.stage
  vpc_id         = var.vpc_id
  public_subnets = var.public_subnets
}

module "route53_record" {
  source                      = "../../modules/route53"
  hostzone_id                 = var.hostzone_id
  stage                       = local.stage
  hostzone_name               = var.hostzone_name
  app_lb_zone_id              = module.alb.app_alb.zone_id
  app_lb_zone_name            = module.alb.app_alb.dns_name
  fixed_response_lb_zone_id   = module.alb.fixed_response_alb.zone_id
  fixed_response_lb_zone_name = module.alb.fixed_response_alb.dns_name
}

module "secrets" {
  source             = "../../modules/secrets"
  app_name           = local.app_name
  stage              = local.stage
  cognito_userool_id = var.cognito_userool_id
  cognito_client_id  = var.cognito_client_id
  find_place_api_key = var.find_place_api_key
  resas_api_key      = var.resas_api_key
  db_user            = var.db_user
  db_password        = var.db_password
  db_host            = module.db.aurora_serverless_mysql80.endpoint
  db_port            = module.db.aurora_serverless_mysql80.port
}

module "monitoring" {
  source              = "../../modules/monitoring"
  app_name            = local.app_name
  stage               = local.stage
  app_tg_1_arn_suffix = module.app.tg_1.arn_suffix
  ecs_cluster_name    = module.app.ecs_cluster_name
  ecs_service_name    = module.app.ecs_service_name
}