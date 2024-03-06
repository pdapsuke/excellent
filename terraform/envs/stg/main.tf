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
  aws_region      = data.aws_region.current.name
  account_id      = data.aws_caller_identity.self.account_id
  app_name        = replace(lower("excellent"), "-", "")
  stage           = "stg"
  vpc_cidr_block  = "192.168.0.0/16"
}

// 変数定義
variable "vpc_id" { type = string }
variable "private_subnets" { type = list(string) }
variable "db_user" { type = string }
variable "db_password" { type = string }
variable "app_image_uri" { type = string }
variable "public_subnets" { type = list(string) }

output db_secrets_manager_arn {
  value = module.db.db_secrets_manager_arn
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
