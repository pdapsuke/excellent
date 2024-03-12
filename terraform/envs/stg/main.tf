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
  aws_region     = data.aws_region.current.name
  account_id     = data.aws_caller_identity.self.account_id
  app_name       = replace(lower("excellent"), "-", "")
  stage          = "stg"
  vpc_cidr_block = "192.168.0.0/16"
}

// 変数定義
variable "vpc_id" { type = string }
variable "private_subnets" { type = list(string) }
variable "db_user" { type = string }
variable "db_password" { type = string }
variable "front_app_image_uri" { type = string }
variable "api_app_image_uri" { type = string }
variable "nginx_app_image_uri" { type = string }
variable "public_subnets" { type = list(string) }
variable "hostzone_id" { type = string }
variable "hostzone_name" { type = string }

output "db_secrets_manager_arn" {
  value = module.db.db_secrets_manager_arn
}

module "base" {
  source   = "../../modules/base"
  app_name = local.app_name
  stage    = local.stage
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
  source              = "../../modules/app"
  app_name            = local.app_name
  stage               = local.stage
  account_id          = local.account_id
  front_app_image_uri = var.front_app_image_uri
  api_app_image_uri   = var.api_app_image_uri
  nginx_app_image_uri = var.nginx_app_image_uri
  vpc_id              = var.vpc_id
  subnets             = var.public_subnets
  ingress_cidr_blocks = [local.vpc_cidr_block]
  app_alb_arn         = module.alb.app_alb.arn
  sns_topic_arn       = module.base.sns_topic_arn
  env = {
    "MODE" : local.stage,
    "SNS_ARN" : module.base.sns_topic_arn,
    "DB_NAME" : local.stage,
    "DB_SECRET_NAME" : "/${local.app_name}/${local.stage}/db",
    "COGNITO_USERPOOL_ID" : "***REMOVED***",
    "COGNITO_CLIENT_ID" : "***REMOVED***",
    "FIND_PLACE_URL" : "https://maps.googleapis.com/maps/api/place/textsearch/json",
    "PLACE_DETAILS_URL" : "https://maps.googleapis.com/maps/api/place/details/json",
    "FIND_PLACE_API_KEY" : "***REMOVED***",
    "PHOTO_REFERENCE_URL" : "https://maps.googleapis.com/maps/api/place/photo",
    "AWS_REGION" : "ap-northeast-1"
    "NUXT_CLIENT_BASE_URL" : "http://${module.route53_record.route53_record.name}/api/v1"
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
  source        = "../../modules/route53"
  hostzone_id   = var.hostzone_id
  stage         = local.stage
  hostzone_name = var.hostzone_name
  lb_zone_id    = module.alb.app_alb.zone_id
  lb_zone_name  = module.alb.app_alb.dns_name
}