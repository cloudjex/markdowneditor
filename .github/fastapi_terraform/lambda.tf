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

resource "aws_iam_role_policy_attachment" "logs_basic_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "dynamodb_rw" {
  name = "${var.project_name}-dynamodb-rw"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ],
        Resource = [
          "*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "ses_basic_email" {
  name = "${var.project_name}-ses-send-email"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ],
        Resource = "*"
      }
    ]
  })
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
  retention_in_days = 14
  tags = {
    Name = "${var.project_name}"
  }
}
