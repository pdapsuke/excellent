#!/bin/bash

set -ex

APP_ROOT=$(cd $(dirname $0)/..; pwd)
SCRIPT_DIR="${APP_ROOT}/bin"
API_DIR="${APP_ROOT}/api"

source $SCRIPT_DIR/lib/fetch_db_secret.sh

# データベース削除
MYSQL_PWD=$DB_PASSWORD mysql -u $DB_USER -h $DB_HOST -P $DB_PORT -e "DROP DATABASE IF EXISTS $DB_NAME"

# データベース作成
MYSQL_PWD=$DB_PASSWORD mysql -u $DB_USER -h $DB_HOST -P $DB_PORT -e "CREATE DATABASE IF NOT EXISTS $DB_NAME"

cd $API_DIR

# マイグレーション
alembic upgrade head