data "aws_ecr_repository" "mock_provider_registry" {
  name = var.registry_id
}

resource "aws_ecs_task_definition" "mock-provider" {
  family                   = var.prefix
  network_mode             = "awsvpc"
  // ARN of IAM role that allows your Amazon ECS container task to make calls to other AWS services.
  task_role_arn            = aws_iam_role.task_role.arn
  //ARN of the task execution role that the Amazon ECS container agent and the Docker daemon can assume.
  execution_role_arn       = aws_iam_role.task_execution_role.arn
  requires_compatibilities = [
    "FARGATE"]
  cpu                      = 256
  memory                   = 512

  container_definitions = jsonencode([
    {
      name      = local.service_name
      image     = "${data.aws_ecr_repository.mock_provider_registry.repository_url}:${var.image_version}"
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
        }
      ]

      environment : [
        {
          "name" : "PORT",
          "value" : tostring(var.container_port)
        }
      ],
      logConfiguration : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-create-group" : "true",
          "awslogs-group" : aws_cloudwatch_log_group.container_log_group.name
          "awslogs-region" : "eu-west-2",
          // TODO: Fargate creates it's own stream. Do we need to create our own? -> set awslogs-create-group to false and see if we can use our own stream which has retention
          "awslogs-stream-prefix" : aws_cloudwatch_log_stream.container_log_stream.name
        }
      }
    }
  ])
}
