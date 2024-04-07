output "route53_record_app_alb" {
  value = aws_route53_record.www1
}

output "route53_record_fixed_response_alb" {
  value = aws_route53_record.www2
}