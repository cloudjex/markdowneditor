resource "aws_lambda_function" "fastapi_lambda" {
  function_name    = "cloudjex-lambda"
  role             = "arn:aws:iam::736798815711:role/cloudjex-lambda"
  runtime          = "python3.13"
  handler          = "app.handler"
  filename         = "${path.module}/../build/deploy.zip"
  source_code_hash = filebase64sha256("${path.module}/../build/deploy.zip")
  timeout          = 30
  tags = {
    Name : "cork-up"
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.fastapi_lambda.function_name}"
  retention_in_days = 30
  tags = {
    Name : "cloudjex"
  }
}
