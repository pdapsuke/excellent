resource "aws_rds_cluster" "aurora_serverless_mysql80" {
  cluster_identifier = "${var.app_name}-${var.stage}-aurora-serverless-v2-mysql80-cluster"

  engine = "aurora-mysql"
  engine_version = "8.0.mysql_aurora.3.05.2"

  database_name   = var.db_name
  master_username = var.db_user
  master_password = var.db_password
  port            = local.db_port

  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.aurora_serverless_mysql80.name

  backup_retention_period = 7

  // aws_rds_cluster_instance.db_subnet_group_nameと一致している必要がある
  db_subnet_group_name   = aws_db_subnet_group.aurora_serverless_mysql80.name
  vpc_security_group_ids = [aws_security_group.aurora_serverless_mysql80.id]

  // スケールアップ/ダウン時の最小ACU, 最大ACUを定義
  serverlessv2_scaling_configuration {
    min_capacity = 0.5 // 0.5 ~
    max_capacity = 1.0 // ~ 128
  }

  // 削除時にスナップショットを作成しない
  skip_final_snapshot = true

  lifecycle {
    ignore_changes = [
      master_password // パスワードが変更されていても無視する
    ]
  }
}

resource "aws_rds_cluster_parameter_group" "aurora_serverless_mysql80" {
  name   = "${var.app_name}-${var.stage}-aurora-serverless-v2-mysql80-cluster-parameter-group"
  family = "aurora-mysql8.0"

  parameter {
    name         = "time_zone"
    value        = "Asia/Tokyo"
    apply_method = "immediate"
  }
  parameter {
    name  = "character_set_client"
    value = "utf8mb4"
  }
  parameter {
    name  = "character_set_connection"
    value = "utf8mb4"
  }
  parameter {
    name  = "character_set_database"
    value = "utf8mb4"
  }
  parameter {
    name  = "character_set_filesystem"
    value = "binary"
  }
  parameter {
    name  = "character_set_results"
    value = "utf8mb4"
  }
  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
  }
  parameter {
    name  = "collation_connection"
    value = "utf8mb4_bin"
  }
  parameter {
    name  = "collation_server"
    value = "utf8mb4_bin"
  }
}

resource "aws_db_subnet_group" "aurora_serverless_mysql80" {
  name       = "${var.app_name}-${var.stage}-aurora-serverless-v2-mysql80-sg"
  subnet_ids = var.private_subnets
}

resource "aws_security_group" "aurora_serverless_mysql80" {
  name   = "${var.app_name}-${var.stage}-aurora-serverless-v2-mysql80"
  vpc_id = var.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = local.db_port
    to_port     = local.db_port
    protocol    = "tcp"
    cidr_blocks = var.ingress_cidr_blocks
  }
  tags = {
    "Name" = "${var.app_name}-${var.stage}-aurora-serverless-v2-mysql80"
  }
}

// DBインスタンス
resource "aws_rds_cluster_instance" "aurora_serverless_mysql80" {
  count              = var.instance_num
  cluster_identifier = aws_rds_cluster.aurora_serverless_mysql80.id
  // Aurora Serverless V2を利用する場合は db.serverless 固定
  instance_class = "db.serverless"
  engine         = aws_rds_cluster.aurora_serverless_mysql80.engine
  engine_version = aws_rds_cluster.aurora_serverless_mysql80.engine_version

  // クラスタと同じサブネットグループを利用
  db_subnet_group_name = aws_rds_cluster.aurora_serverless_mysql80.db_subnet_group_name
  // パブリックアクセス不可
  publicly_accessible = false
}