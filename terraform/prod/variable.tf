variable "environment_prefix" {
  type        = string
  description = "環境名プレフィックス"
  default     = "prod"
}

variable "app_name_prefix" {
  type        = string
  description = "アプリケーションメイプレフィックス"
  default     = "linebot"
}

variable "labels" {
  type = map(string)
  default = {
    environment = "prod-linebot"
    managed_by  = "terraform"
  }
}