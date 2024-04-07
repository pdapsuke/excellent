// アプリ用ALBへのルーティング（Primary）
resource "aws_route53_record" "www1" {
  zone_id = var.hostzone_id
  name    = "bassen.${var.stage}.${var.hostzone_name}"
  type    = "A"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier = "www1"
  alias {
    name                   = var.app_lb_zone_name
    zone_id                = var.app_lb_zone_id
    evaluate_target_health = true
  }
}

// 固定レスポンス用ALBへのルーティング（Secondary）
resource "aws_route53_record" "www2" {
  zone_id = var.hostzone_id
  name    = "bassen.${var.stage}.${var.hostzone_name}"
  type    = "A"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "www2"
  alias {
    name                   = var.fixed_response_lb_zone_name
    zone_id                = var.fixed_response_lb_zone_id
    evaluate_target_health = false
  }
}