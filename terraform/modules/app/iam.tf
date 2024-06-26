// タスク実行ロール
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.app_name}-${var.stage}-EcsTaskExecutionRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com",
        },
        "Action" : "sts:AssumeRole",
      }
    ]
  })
}

resource "aws_iam_policy" "ecs_task_execution_policy" {
  name = "${var.app_name}-${var.stage}-EcsTaskExecutionPolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        "Resource" : [
          "arn:aws:secretsmanager:ap-northeast-1:${var.account_id}:secret:/${var.app_name}/*"
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        "Resource": "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_execution_policy.arn
}

// タスクロール
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.app_name}-${var.stage}-EcsTaskRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs-tasks.amazonaws.com",
        },
        "Action" : "sts:AssumeRole",
      }
    ]
  })
}

resource "aws_iam_policy" "ecs_task_policy" {
  name = "${var.app_name}-${var.stage}-EcsTaskPolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        "Resource" : [
          "arn:aws:secretsmanager:ap-northeast-1:${var.account_id}:secret:/${var.app_name}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_ecs_task_role_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_task_policy.arn
}