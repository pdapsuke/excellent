output "ecs_cluster_name" {
  value = aws_ecs_cluster.app_cluster.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app_service.name
}

output "ecs_task_family" {
  value = aws_ecs_task_definition.app_task_definition.family
}

output "ecs_task_revision" {
  value = aws_ecs_task_definition.app_task_definition.revision
}

output "tg_1" {
  value = aws_lb_target_group.app_tg_1
}

output "esc_task_definition_arn" {
  value = aws_ecs_task_definition.app_task_definition.arn
}
