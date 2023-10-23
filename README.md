# 開発環境準備
## mysqlの起動

※ 起動していない場合のみ

```bash
./bin/mysql.sh
```

# ■ テーブルの作成

```bash
# 開発用shellを起動
./bin/run.sh --mode shell

# データベースを作成
MYSQL_PWD=$DB_PASSWORD mysql -u $DB_USER -h $DB_HOST -P $DB_PORT -e "CREATE DATABASE IF NOT EXISTS $DB_NAME"

# マイグレーション
(cd api;alembic upgrade head)

exit
```

## アプリの起動

アプリを起動して、ブラウザで確認しながら実装していきましょう

```bash
# アプリを起動
./bin/run.sh --mode app
```

http://127.0.0.1:8018/docs にブラウザでアクセス
