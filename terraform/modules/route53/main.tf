resource "aws_route53_record" "www" {
  zone_id = var.hostzone_id
  name    = "bassen.${var.stage}.${var.hostzone_name}"
  type    = "A"

  alias {
    name                   = var.lb_zone_name
    zone_id                = var.lb_zone_id
    evaluate_target_health = true
  }
}