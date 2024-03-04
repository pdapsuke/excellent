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

output "account_id" {
  value = data.aws_caller_identity.self.account_id
}

output "aws_region" {
  value = data.aws_region.current.name
}