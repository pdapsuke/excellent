// 秘匿性が高いコンテナの環境変数をsecrets managerで保持
resource "aws_secretsmanager_secret" "env_variables" {
  name                           = "/${var.app_name}/${var.stage}/env"
  recovery_window_in_days        = 0
  force_overwrite_replica_secret = true
}

resource "aws_secretsmanager_secret_version" "env_variables" {
  secret_id = aws_secretsmanager_secret.env_variables.id
  secret_string = jsonencode({
    cognito_userool_id     = var.cognito_userool_id
    cognito_client_id = var.cognito_client_id
    find_place_url = var.find_place_url
    place_details_url = var.place_details_url
    find_place_api_key = var.find_place_api_key
    photo_reference_url = var.photo_reference_url
  })
}

// DBのログイン情報をsecrests managerで保持
resource "aws_secretsmanager_secret" "aurora_serverless_mysql80" {
  name                           = "/${var.app_name}/${var.stage}/db"
  recovery_window_in_days        = 0
  force_overwrite_replica_secret = true
}

resource "aws_secretsmanager_secret_version" "aurora_serverless_mysql80" {
  secret_id = aws_secretsmanager_secret.aurora_serverless_mysql80.id
  secret_string = jsonencode({
    db_user     = var.db_user
    db_password = var.db_password
    db_host     = var.db_host
    db_port     = var.db_port
  })
}