resource "aws_lb_listener" "api_http_80" {
  load_balancer_arn = aws_lb.alb.arn
  port              = var.listener_port
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.http_mock_provider_tg.arn
  }
}
