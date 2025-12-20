resource "aws_dynamodb_table" "users_table" {
  name         = "${var.project_name}-users-table"
  billing_mode = "PROVISIONED"

  read_capacity  = 1
  write_capacity = 1

  hash_key = "email"
  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name = "${var.project_name}"
  }
}

resource "aws_dynamodb_table" "trees_table" {
  name         = "${var.project_name}-trees-table"
  billing_mode = "PROVISIONED"

  read_capacity  = 1
  write_capacity = 1

  hash_key = "email"
  attribute {
    name = "email"
    type = "S"
  }

  tags = {
    Name = "${var.project_name}"
  }
}

resource "aws_dynamodb_table" "nodes_table" {
  name         = "${var.project_name}-nodes-table"
  billing_mode = "PROVISIONED"

  read_capacity  = 1
  write_capacity = 1

  hash_key = "email"
  attribute {
    name = "email"
    type = "S"
  }
  range_key = "id"
  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name = "${var.project_name}"
  }
}
