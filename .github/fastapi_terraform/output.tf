output "api_endpoint" {
  value = "https://${aws_api_gateway_rest_api.rest_api.id}.execute-api.us-east-1.amazonaws.com/${aws_api_gateway_stage.stage.stage_name}"
}

output "custom_api_url" {
  value = "https://${aws_api_gateway_domain_name.custom_domain.domain_name}/${aws_api_gateway_stage.stage.stage_name}"
}
