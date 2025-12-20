resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}"
  }
}

resource "aws_iam_role_policy_attachment" "logs_full_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_role_policy_attachment" "dynamodb_full_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_lambda_function" "fastapi_lambda" {
  function_name    = "${var.project_name}-lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  runtime          = "python3.13"
  handler          = "app.handler"
  filename         = "${path.module}/../build/deploy.zip"
  source_code_hash = filebase64sha256("${path.module}/../build/deploy.zip")
  timeout          = 30
  tags = {
    Name = "${var.project_name}"
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.fastapi_lambda.function_name}"
  retention_in_days = 30
  tags = {
    Name = "${var.project_name}"
  }
}
