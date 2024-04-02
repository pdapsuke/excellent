/**
 * AutoScaling用role
 */
resource "aws_iam_role" "ecs_autoscaling_role" {
  name = "${var.app_name}-${var.stage}-EcsAutoscalingRole"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ecs.application-autoscaling.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "ecs_autoscaling_policy" {
  name = "${var.app_name}-${var.stage}-EcsAutoscalingPolicy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "ecs:DescribeServices",
          "ecs:UpdateService",
          "cloudwatch:PutMetricAlarm",
          "cloudwatch:DescribeAlarms",
          "cloudwatch:DeleteAlarms"
        ],
        "Resource" : [
          "*"
        ]
      }
    ]
  })
}