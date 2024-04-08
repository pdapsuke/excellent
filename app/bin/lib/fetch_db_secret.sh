#!/bin/bash

if [ "$MODE" != "local" ]; then
  SECRET_STRING="$(aws secretsmanager get-secret-value --secret-id "$DB_SECRET_NAME" --query 'SecretString' --output text)"
	DB_PASSWORD=$(echo "$SECRET_STRING" | jq -r '.db_password')
	DB_USER=$(echo "$SECRET_STRING" | jq -r '.db_user')
	DB_HOST=$(echo "$SECRET_STRING" | jq -r '.db_host')
	DB_PORT=$(echo "$SECRET_STRING" | jq -r '.db_password')
fi