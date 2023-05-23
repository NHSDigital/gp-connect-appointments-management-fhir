resource "aws_acm_certificate" "service_certificate" {
  domain_name               = var.api_domain_name
  subject_alternative_names = []
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "api_domain" {
  zone_id = var.zone_id
  name    = aws_apigatewayv2_domain_name.service_api_domain_name.domain_name
  type    = "A"
  alias {
    evaluate_target_health = true
    name                   = aws_apigatewayv2_domain_name.service_api_domain_name.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.service_api_domain_name.domain_name_configuration[0].hosted_zone_id
  }
}

resource "aws_route53_record" "dns_validation" {
  for_each = {
  for dvo in aws_acm_certificate.service_certificate.domain_validation_options : dvo.domain_name => {
    name   = dvo.resource_record_name
    record = dvo.resource_record_value
    type   = dvo.resource_record_type
  }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [
    each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.zone_id
}
