// ECSのオートスケーリング対象設定
resource "aws_appautoscaling_target" "ecs_appautoscaling_target" {
  // オートスケーリング対象のサービス名を指定
  service_namespace = "ecs"
  // "service/クラスター名/サービス名" 形式で紐付けたいECSのサービスを指定
  resource_id = "service/${var.ecs_cluster_name}/${var.ecs_service_name}"
  // オートスケーリングを実行する対象を指定
  scalable_dimension = "ecs:service:DesiredCount"
  role_arn           = aws_iam_role.ecs_autoscaling_role.arn
  // オートスケーリングさせる時の最小値と最大値
  min_capacity = 1
  max_capacity = var.max_capacity

  depends_on = [
    aws_iam_policy.ecs_autoscaling_policy
  ]
}

// スケーリングポリシー設定
resource "aws_appautoscaling_policy" "ecs_1_policy" {
  name               = "${var.app_name}-${var.stage}-AccessCountTracking"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_appautoscaling_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_appautoscaling_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_appautoscaling_target.service_namespace

  // https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appautoscaling_policy#target_tracking_scaling_policy_configuration
  target_tracking_scaling_policy_configuration {
    // 1台あたりの分間リクエスト数を avg_request_count_per_target に保つ
    target_value = var.avg_request_count_per_target
    scale_in_cooldown = 300
    scale_out_cooldown = 180
    customized_metric_specification {
      // app_tg_1の「リクエスト数/ターゲット台数」を取得
      metrics {
        id    = "${var.app_name}_${var.stage}_m1"
        label = "${var.app_name}-${var.stage}-app-tg-1 RequestCountPerTarget"

        metric_stat {
          metric {
            namespace   = "AWS/ApplicationELB"
            metric_name = "RequestCountPerTarget"

            dimensions {
              name  = "TargetGroup"
              value = var.app_tg_1_arn_suffix
            }
          }
          stat = "Sum"
          // https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html
          unit = "None"
        }
        return_data = true
      }
    }
  }
}