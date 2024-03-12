variable "app_name" {}
variable "stage" {}

// セキュリティグループが所属するVPC
variable "vpc_id" {}

// ALBが所属するサブネット
variable "public_subnets" {
  type = list(string)
}

// ALBがアクセスを許可するIPアドレス
variable "ingress_rules_cidr_blocks" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}