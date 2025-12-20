resource "aws_api_gateway_rest_api" "rest_api" {
  name = "cloudjex-apigateway"
  endpoint_configuration {
    types = ["EDGE"]
  }
  tags = {
    Name = "cloudjex"
  }
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy_method" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.proxy_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.fastapi_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [aws_api_gateway_integration.lambda]
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
}

resource "aws_api_gateway_stage" "stage" {
  stage_name    = "api"
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}

resource "aws_lambda_permission" "apigw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fastapi_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*/*"
}

resource "aws_api_gateway_domain_name" "custom_domain" {
  domain_name     = "api.cloudjex.com"
  certificate_arn = "arn:aws:acm:us-east-1:736798815711:certificate/da7c6c5c-cb24-4559-871a-724a26dbcff0"

  endpoint_configuration {
    types = ["EDGE"]
  }

  tags = {
    Name = "cloudjex"
  }
}

resource "aws_api_gateway_base_path_mapping" "custom_mapping" {
  api_id      = aws_api_gateway_rest_api.rest_api.id
  domain_name = aws_api_gateway_domain_name.custom_domain.domain_name
  stage_name  = aws_api_gateway_stage.stage.stage_name
  base_path = "api"
}
