resource "aws_sns_topic" "this" {
  name = "${var.app_name}-${var.stage}-topic"
  lifecycle {
    ignore_changes = all
  }
}