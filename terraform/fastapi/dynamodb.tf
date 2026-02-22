resource "aws_dynamodb_table" "table" {
  name         = "${var.project_name}-table"
  billing_mode = "PROVISIONED"

  read_capacity  = 1
  write_capacity = 1

  hash_key = "PK"
  attribute {
    name = "PK"
    type = "S"
  }

  range_key = "SK"
  attribute {
    name = "SK"
    type = "S"
  }

  tags = {
    Name = "${var.project_name}"
  }
}
