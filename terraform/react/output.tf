output "s3_bucket" {
  value = aws_s3_bucket.bucket.bucket
}

output "cloudfront_id" {
  value = aws_cloudfront_distribution.cdn.id
}

output "cloudfront_url" {
  value = "https://${aws_cloudfront_distribution.cdn.domain_name}"
}

output "cloudfront_custom_url" {
  value = "https://${var.custom_domain}"
}
