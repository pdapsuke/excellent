// 本番用リスナーにアタッチするターゲットグループ
resource "aws_lb_target_group" "app_tg_1" {
  name        = "${var.app_name}-${var.stage}-app-tg-1"
  port        = "80"
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    interval            = 30
    timeout             = 5
    healthy_threshold   = 3
    unhealthy_threshold = 3
    path                = "/healthCheck"
    protocol            = "HTTP"
    matcher             = "200"
  }

  tags = {
    Name = "${var.app_name}-${var.stage}-app-tg-1"
  }
}

// HTTPS:443 本番用リスナー
resource "aws_lb_listener" "app_listener_green_https" {
  // use_https_listener = "1" のときのみ作成
  count             = local.use_https_listener
  load_balancer_arn = var.app_alb_arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.app_tg_1.arn
        weight = 1
      }
    }
  }
  lifecycle {
    ignore_changes = [
      certificate_arn,
      default_action
    ]
  }
}

// HTTP:80 本番用リスナー (HTTPS:443 にリダイレクト)
resource "aws_lb_listener" "app_listener_redirect" {
  // use_https_listener = "1" のときのみ作成
  count             = local.use_https_listener
  load_balancer_arn = var.app_alb_arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
  lifecycle {
    ignore_changes = [
      default_action
    ]
  }
}

// HTTP:80 本番用用リスナー
resource "aws_lb_listener" "app_listener_green_http" {
  // use_http_listener = "1" のときのみ作成
  count             = local.use_http_listener
  load_balancer_arn = var.app_alb_arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "forward"
    forward {
      target_group {
        arn    = aws_lb_target_group.app_tg_1.arn
        weight = 1
      }
    }
  }
  lifecycle {
    ignore_changes = [
      default_action
    ]
  }
}

// HTTPS:443 固定レスポンス用リスナー
resource "aws_lb_listener" "fixed_response_listener_https" {
  count             = local.use_https_listener
  load_balancer_arn = var.fixed_response_alb_arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "サービスは一時停止しています"
      status_code  = "500"
    }
  }

  lifecycle {
    ignore_changes = [
      certificate_arn,
      default_action
    ]
  }
}

// HTTP:80 固定レスポンス用リスナー (HTTPS:443 にリダイレクト)
resource "aws_lb_listener" "fixed_response_listener_redirect" {
  count             = local.use_https_listener
  load_balancer_arn = var.fixed_response_alb_arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
  lifecycle {
    ignore_changes = [
      default_action
    ]
  }
}

// HTTP:80 固定レスポンス用リスナー
resource "aws_lb_listener" "fixed_response_listener_http" {
  count             = local.use_http_listener
  load_balancer_arn = var.fixed_response_alb_arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "サービスは一時停止しています"
      status_code  = "500"
    }
  }
  lifecycle {
    ignore_changes = [
      default_action
    ]
  }
}

// ECSクラスター
resource "aws_ecs_cluster" "app_cluster" {
  name = "${var.app_name}-${var.stage}-app"

  setting {
    // CloudWatch Container Insights を有効化
    name  = "containerInsights"
    value = "enabled"
  }
}

// aws_ecs_cluster_capacity_providers: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_cluster_capacity_providers
resource "aws_ecs_cluster_capacity_providers" "app_cluster_capacity_providers" {
  cluster_name = aws_ecs_cluster.app_cluster.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1 // 指定されたキャパシティプロバイダ上で実行するタスクの最小数
    weight            = 1 // 指定されたキャパシティプロバイダを使用すべきタスク総数の割合
    capacity_provider = "FARGATE"
  }

  default_capacity_provider_strategy {
    weight            = 2               // FARGATE_SPOTの方が優先される
    capacity_provider = "FARGATE_SPOT"  // タスクが中断される可能性があるが、コストが安い
  }
}

// ロググループ
resource "aws_cloudwatch_log_group" "ecs_task_app_log_group" {
  name              = "${var.app_name}/${var.stage}/app/ecs-task"
  retention_in_days = 365  // 保持期間
}

// タスク定義
resource "aws_ecs_task_definition" "app_task_definition" {
  family = "${var.app_name}-${var.stage}-app"

  // タスクが必要とする起動タイプ
  requires_compatibilities = ["FARGATE"]

  // タスクサイズ:
  cpu    = 4096
  memory = 8192

  // ネットワークモード
  network_mode = "awsvpc"

  // ランタイムプラットフォーム: コンテナのホストOSの情報
  runtime_platform { #
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  // タスクに割り当てられるストレージ容量 (GiB)
  ephemeral_storage {
    size_in_gib = 32
  }

  // タスク実行ロール
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

  // タスクロール
  task_role_arn = aws_iam_role.ecs_task_role.arn

  // コンテナ定義:
  container_definitions = jsonencode([
    {
      name      = local.front_container_name  // フロントエンドのコンテナ
      image     = "${var.front_app_image_uri}:${var.container_image_version}"
      cpu       = 2048
      memory    = 3072
      essential = true // essential=Trueのコンテナが停止した場合、タスク全体が停止する
      // 3000番ポートをホストにマッピング
      portMappings = [
        {
          containerPort = local.front_container_port // フロントエンドのコンテナ
          hostPort      = 3000
        }
      ]
      environment = [
        for k, v in var.env_front : {
          name  = k
          value = v
        }
      ]
      // secrets managerから秘匿情報を取得して環境変数にセット
      secrets     = [
        for k, v in var.secrets_front : {
          name  = k
          valueFrom = v
        }
      ]

      // 終了シグナル発進時、この秒数を超えてコンテナが終了しない場合は強制終了させる
      stopTimeout = 30

      // ログの設定
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_app_log_group.name
          awslogs-region        = "ap-northeast-1"
          awslogs-stream-prefix = "front"
        }
      }
    },
    {
      name      = local.api_container_name // バックエンドのコンテナ
      image     = "${var.api_app_image_uri}:${var.container_image_version}"
      cpu       = 1024
      memory    = 3072
      essential = true
      portMappings = [
        {
          containerPort = local.api_container_port
          hostPort      = 8018
        }
      ]
      environment = [
        for k, v in var.env_api : {
          name  = k
          value = v
        }
      ]
      secrets     = [
        for k, v in var.secrets_api : {
          name  = k
          valueFrom = v
        }
      ]
      stopTimeout = 30
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_app_log_group.name
          awslogs-region        = "ap-northeast-1"
          awslogs-stream-prefix = "api"
        }
      }
    },
    {
      name      = local.nginx_container_name  // nginxのコンテナ
      image     = "${var.nginx_app_image_uri}:${var.container_image_version}"
      cpu       = 1024
      memory    = 2048
      essential = true
      portMappings = [
        {
          containerPort = local.nginx_container_port
          hostPort      = 80
        }
      ]
      stopTimeout = 30
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_app_log_group.name
          awslogs-region        = "ap-northeast-1"
          awslogs-stream-prefix = "nginx"
        }
      }
    }
  ])
}

// ECSサービス用セキュリティグループ
resource "aws_security_group" "esc_service_sg" {
  name   = "${var.app_name}-${var.stage}-app-EcsService-sg"
  vpc_id = var.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}-${var.stage}-app-EcsService-sg"
  }
}

// サービス
resource "aws_ecs_service" "app_service" {
  name             = "${var.app_name}-${var.stage}-app"
  cluster          = aws_ecs_cluster.app_cluster.id
  task_definition  = aws_ecs_task_definition.app_task_definition.arn
  desired_count    = 1  // 起動するタスク数
  platform_version = "1.4.0"
  launch_type      = "FARGATE"
  scheduling_strategy = "REPLICA" // クラスター全体で必要数のタスクを維持する

  // 新しくタスクが立ち上がった際、この秒数だけヘルスチェックの失敗を無視する
  # health_check_grace_period_seconds = 300

  network_configuration {
    subnets          = var.subnets
    security_groups  = [aws_security_group.esc_service_sg.id]
    assign_public_ip = true // パブリックサブネットに配置するため
  }

  // 本番用のターゲットグループにアタッチ
  load_balancer {
    target_group_arn = aws_lb_target_group.app_tg_1.arn
    container_name   = local.nginx_container_name
    container_port   = 80
  }

  // デプロイ中にサービス内で実行され、健全な状態を維持しなければならない実行タスク数の下限 (%)
  deployment_minimum_healthy_percent = 100

  // デプロイ中にサービス内で実行可能な実行タスク数の上限 (%)
  deployment_maximum_percent = 200

  // デバッグ用の設定
  enable_execute_command = true

  lifecycle {
    // Blue/Greenデプロイで変更をデプロイするので、terraformの管理対象から外す
    ignore_changes = [
      load_balancer,
      desired_count,
      task_definition,
    ]
  }
}