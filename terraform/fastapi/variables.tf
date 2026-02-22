variable "project_name" {
  default = "cloudjex"
}

variable "custom_domain" {
  default = "api.cloudjex.com"
}

variable "CLOUDJEX_JWT_KEY" {
  type = string
}

variable "CLOUDJEX_SMTP_PASSWORD" {
  type = string
}
