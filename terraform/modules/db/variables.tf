variable "app_name" {}
variable "stage" {}

// データベースを作成するVPC
variable "vpc_id" {}

// データベースを作成するサブネット
variable "private_subnets" {
  type = list(any)
}

// データベース名
variable "db_name" {}

// データベースのユーザー名
variable "db_user" {}

// データベースのパスワード
variable "db_password" {}

// データベースへのアクセスを許可するCIDRブロック
variable "ingress_cidr_blocks" {
  type = list(string)
}

// データベースのインスタンス数
variable "instance_num" {
  type = number
}

locals {
  // データベースのポート番号
  db_port = 3306
}