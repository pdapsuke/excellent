output env_secrets_manager_arn {
  value = aws_secretsmanager_secret.env_variables.arn
}

output db_secrets_manager_arn {
  value = aws_secretsmanager_secret.aurora_serverless_mysql80.arn
}