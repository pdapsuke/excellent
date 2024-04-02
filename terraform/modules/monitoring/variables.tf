variable "app_name" {}
variable "stage" {}

// ECSクラスタ名
variable "ecs_cluster_name" {}

// ECSサービス名
variable "ecs_service_name" {}

variable "app_tg_1_arn_suffix" {}

// オートスケーリングの最大台数
variable "max_capacity" {
  type    = number
  default = 20
}

// ターゲット当たりの分間リクエスト数がこの値になるようにオートスケーリングする
variable "avg_request_count_per_target" {
  type    = number
  default = 300  // 秒間5リクエスト
}